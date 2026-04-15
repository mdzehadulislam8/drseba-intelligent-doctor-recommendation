import json
import pickle as pk
import warnings
from functools import lru_cache
from pathlib import Path

import pandas as pd
from django.http import FileResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'doctor_ai_full_package.pkl'
DATA_PATH = BASE_DIR / 'data' / 'Dr.Seba_500_Organized_Final.xlsx'
DEMO_UI_DIR = BASE_DIR / 'demo_ui'


@lru_cache(maxsize=1)
def get_runtime():
    with open(MODEL_PATH, 'rb') as f:
        package = pk.load(f)

    model = package['model']
    le_spec = package['le_spec']
    le_hosp = package['le_hosp']
    feature_encoders = package['feature_encoders']
    features = package['features']

    df = pd.read_excel(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df['online_consultation'] = df['online_consultation'].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)
    df['emergency_service'] = df['emergency_service'].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)
    df['specialization_group'] = le_spec.transform(df['specialization_group'].astype(str))

    return {
        'model': model,
        'le_spec': le_spec,
        'le_hosp': le_hosp,
        'feature_encoders': feature_encoders,
        'features': features,
        'df': df,
    }


def get_options_data():
    runtime = get_runtime()
    df = runtime['df']
    le_spec = runtime['le_spec']
    return {
        'districts': sorted(df['district'].unique().tolist()),
        'thanas': sorted(df['thana'].unique().tolist()),
        'specializations': sorted(le_spec.classes_.tolist()),
    }


def get_thanas_for_district(district):
    runtime = get_runtime()
    df = runtime['df']
    return sorted(df[df['district'] == district]['thana'].unique().tolist())


def get_recommendations(user_input, top_n=None):
    runtime = get_runtime()
    df = runtime['df']
    model = runtime['model']
    le_spec = runtime['le_spec']
    le_hosp = runtime['le_hosp']
    feature_encoders = runtime['feature_encoders']
    features = runtime['features']

    temp_df = df.copy()
    temp_df = temp_df[
        (temp_df['district'] == user_input['district'])
        & (temp_df['thana'] == user_input['thana'])
    ]
    temp_df = temp_df[temp_df['consultation_fees'] <= user_input['max_fee']]

    if user_input['online'] == 1:
        temp_df = temp_df[temp_df['online_consultation'] == 1]

    if user_input['emergency'] == 1:
        temp_df = temp_df[temp_df['emergency_service'] == 1]

    try:
        spec_encoded = le_spec.transform([user_input['specialization']])[0]
        temp_df = temp_df[temp_df['specialization_group'] == spec_encoded]
    except Exception:
        return {'error': 'Invalid specialization'}

    if len(temp_df) == 0:
        return {'message': 'No doctors found with these criteria'}

    x_temp = temp_df[features].copy()

    if 'hospital_type' in x_temp.columns:
        hosp_mapping = {label: idx for idx, label in enumerate(le_hosp.classes_)}
        x_temp['hospital_type'] = x_temp['hospital_type'].astype(str).map(hosp_mapping).fillna(-1).astype(int)

    for col in x_temp.columns:
        if col in feature_encoders:
            encoder = feature_encoders[col]
            label_mapping = {label: idx for idx, label in enumerate(encoder.classes_)}
            x_temp[col] = x_temp[col].astype(str).map(label_mapping).fillna(-1).astype(int)

    temp_df['predicted_score'] = model.predict(x_temp)
    result = temp_df.sort_values(by='predicted_score', ascending=False)

    top_doctors = result[
        [
            'doctor_name',
            'specialization_group',
            'rating_avg',
            'experience_years',
            'consultation_fees',
            'predicted_score',
            'hospital_name',
            'full_address',
        ]
    ]

    if top_n is not None:
        top_doctors = top_doctors.head(top_n)

    recommendations = []
    for _, row in top_doctors.iterrows():
        spec_name = le_spec.classes_[int(row['specialization_group'])]
        recommendations.append(
            {
                'doctor_name': str(row['doctor_name']),
                'specialization': str(spec_name),
                'rating_avg': float(row['rating_avg']),
                'experience_years': int(row['experience_years']),
                'consultation_fees': int(row['consultation_fees']),
                'predicted_score': float(row['predicted_score']),
                'hospital_name': str(row['hospital_name']),
                'full_address': str(row['full_address']),
            }
        )

    return {'success': True, 'count': len(recommendations), 'doctors': recommendations}


@require_http_methods(['GET', 'POST'])
def home(request):
    options = get_options_data()

    selected_district = request.POST.get('district') or (options['districts'][0] if options['districts'] else '')
    thanas_for_selected = get_thanas_for_district(selected_district) if selected_district else []
    selected_thana = request.POST.get('thana') or (thanas_for_selected[0] if thanas_for_selected else '')
    if selected_thana not in thanas_for_selected and thanas_for_selected:
        selected_thana = thanas_for_selected[0]
    selected_spec = request.POST.get('specialization') or (
        options['specializations'][0] if options['specializations'] else ''
    )
    if selected_spec not in options['specializations'] and options['specializations']:
        selected_spec = options['specializations'][0]
    max_fee = request.POST.get('maxFee', '2000')
    online = request.POST.get('online') == 'on'
    emergency = request.POST.get('emergency') == 'on'
    top_n = None

    context = {
        'districts': options['districts'],
        'specializations': options['specializations'],
        'thanas': thanas_for_selected,
        'selected_district': selected_district,
        'selected_thana': selected_thana,
        'selected_spec': selected_spec,
        'max_fee': max_fee,
        'online': online,
        'emergency': emergency,
        'top_n': top_n,
        'searched': False,
        'error': '',
        'doctors': [],
    }

    if request.method == 'POST':
        context['searched'] = True
        try:
            max_fee_int = int(max_fee)
            if max_fee_int < 0:
                max_fee_int = 0

            payload = {
                'district': selected_district,
                'thana': selected_thana,
                'specialization': selected_spec,
                'max_fee': max_fee_int,
                'online': 1 if online else 0,
                'emergency': 1 if emergency else 0,
            }
            result = get_recommendations(payload, top_n)
            if result.get('success'):
                context['doctors'] = result['doctors']
            else:
                context['error'] = result.get('message') or result.get('error') or 'No doctors found'
        except Exception as exc:
            context['error'] = str(exc)

    return render(request, 'index.html', context)


@require_GET
def style_css(request):
    return FileResponse(open(DEMO_UI_DIR / 'style.css', 'rb'), content_type='text/css')


@require_GET
def script_js(request):
    return FileResponse(open(DEMO_UI_DIR / 'script.js', 'rb'), content_type='application/javascript')


@require_GET
def api_root(request):
    return JsonResponse(
        {
            'status': 'healthy',
            'message': 'Doctor Recommendation API is running',
            'endpoints': [
                '/api/health',
                '/api/options',
                '/api/thanas/<district>',
                '/api/recommendations',
            ],
        }
    )


@require_GET
def api_health(request):
    return JsonResponse({'status': 'healthy'})


@require_GET
def api_options(request):
    return JsonResponse({'success': True, 'options': get_options_data()})


@require_GET
def api_thanas(request, district):
    thanas = get_thanas_for_district(district)
    if not thanas:
        return JsonResponse({'error': f'No thanas found for {district}'}, status=404)
    return JsonResponse({'district': district, 'thanas': thanas})


@csrf_exempt
@require_http_methods(['POST'])
def api_recommendations(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    required = ['district', 'thana', 'specialization', 'max_fee', 'online', 'emergency']
    for field in required:
        if field not in data:
            return JsonResponse({'error': f'Missing: {field}'}, status=400)

    top_n = data.get('top_n', 5)
    result = get_recommendations(data, top_n)

    if 'error' in result:
        return JsonResponse(result, status=400)
    return JsonResponse(result)
