"""
Doctor Recommendation API - Complete Backend
Uses ML Model + Dataset to recommend doctors
"""

import pickle as pk
import pandas as pd
from flask import Flask, request, jsonify
import json
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

# Initialize Flask
app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'doctor_ai_full_package.pkl'
DATA_PATH = BASE_DIR / 'data' / 'Dr.Seba_500_Organized_Final.xlsx'

# Enforce CORS at WSGI level so every response includes required headers.
class CORSMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def cors_start_response(status, headers, exc_info=None):
            headers.append(('Access-Control-Allow-Origin', '*'))
            headers.append(('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'))
            headers.append(('Access-Control-Allow-Headers', 'Content-Type, Authorization'))
            headers.append(('Access-Control-Max-Age', '86400'))
            return start_response(status, headers, exc_info)

        return self.app(environ, cors_start_response)


app.wsgi_app = CORSMiddleware(app.wsgi_app)


@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_preflight(path):
    return ('', 204)

# Load ML Model and Encoders
print("[STARTUP] Loading ML Model...")
with open(MODEL_PATH, 'rb') as f:
    package = pk.load(f)

model = package["model"]
le_spec = package["le_spec"]
le_hosp = package["le_hosp"]
feature_encoders = package["feature_encoders"]
features = package["features"]
print("[STARTUP] ✅ ML Model loaded!")

# Load Dataset
print("[STARTUP] Loading Dataset...")
df = pd.read_excel(DATA_PATH)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Convert Yes/No to 1/0
df['online_consultation'] = df['online_consultation'].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)
df['emergency_service'] = df['emergency_service'].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)

# Encode specialization
df['specialization_group'] = le_spec.transform(df['specialization_group'].astype(str))
print(f"[STARTUP] ✅ Dataset loaded! ({len(df)} doctors)")


def get_recommendations(user_input, top_n=5):
    """Get doctor recommendations based on criteria"""
    temp_df = df.copy()

    # Filter by location
    temp_df = temp_df[
        (temp_df['district'] == user_input['district']) &
        (temp_df['thana'] == user_input['thana'])
    ]

    # Filter by fees
    temp_df = temp_df[temp_df['consultation_fees'] <= user_input['max_fee']]

    # Filter by services
    if user_input['online'] == 1:
        temp_df = temp_df[temp_df['online_consultation'] == 1]

    if user_input['emergency'] == 1:
        temp_df = temp_df[temp_df['emergency_service'] == 1]

    # Filter by specialization
    try:
        spec_encoded = le_spec.transform([user_input['specialization']])[0]
        temp_df = temp_df[temp_df['specialization_group'] == spec_encoded]
    except:
        return {"error": "Invalid specialization"}

    if len(temp_df) == 0:
        return {"message": "No doctors found with these criteria"}

    # Prepare features for prediction
    X_temp = temp_df[features].copy()
    
    # Encode hospital_type
    if 'hospital_type' in X_temp.columns:
        hosp_mapping = {label: idx for idx, label in enumerate(le_hosp.classes_)}
        X_temp['hospital_type'] = X_temp['hospital_type'].astype(str).map(hosp_mapping).fillna(-1).astype(int)
    
    # Encode other categoricals
    for col in X_temp.columns:
        if col in feature_encoders:
            encoder = feature_encoders[col]
            label_mapping = {label: idx for idx, label in enumerate(encoder.classes_)}
            X_temp[col] = X_temp[col].astype(str).map(label_mapping).fillna(-1).astype(int)

    # ML Prediction
    temp_df['predicted_score'] = model.predict(X_temp)

    # Sort by score
    result = temp_df.sort_values(by='predicted_score', ascending=False)
    
    # Get top N
    top_doctors = result[['doctor_name', 'specialization_group', 'rating_avg', 'experience_years', 'consultation_fees', 
                          'predicted_score', 'hospital_name', 'full_address']].head(top_n)
    
    # Convert to JSON
    recommendations = []
    for idx, row in top_doctors.iterrows():
        # Get original specialization from le_spec classes
        spec_name = le_spec.classes_[int(row['specialization_group'])]
        
        recommendations.append({
            "doctor_name": str(row['doctor_name']),
            "specialization": str(spec_name),
            "rating_avg": float(row['rating_avg']),
            "experience_years": int(row['experience_years']),
            "consultation_fees": int(row['consultation_fees']),
            "predicted_score": float(row['predicted_score']),
            "hospital_name": str(row['hospital_name']),
            "full_address": str(row['full_address'])
        })
    
    return {"success": True, "count": len(recommendations), "doctors": recommendations}


# ============= API ENDPOINTS =============

@app.route('/api', methods=['GET'])
def api_root():
    return jsonify({
        "status": "healthy",
        "message": "Doctor Recommendation API is running",
        "endpoints": [
            "/api/health",
            "/api/options",
            "/api/districts",
            "/api/thanas/<district>",
            "/api/specializations",
            "/api/recommendations"
        ]
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})


@app.route('/api/districts', methods=['GET'])
def get_districts():
    """Get all districts from database"""
    try:
        districts = sorted(df['district'].unique().tolist())
        return jsonify({"success": True, "districts": districts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/thanas/<district>', methods=['GET'])
def get_thanas(district):
    """Get thanas for a district"""
    try:
        thanas = sorted(df[df['district'] == district]['thana'].unique().tolist())
        if not thanas:
            return jsonify({"error": f"No thanas found for {district}"}), 404
        return jsonify({"district": district, "thanas": thanas})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/specializations', methods=['GET'])
def get_specializations():
    """Get all specializations"""
    try:
        specs = sorted(le_spec.classes_.tolist())
        return jsonify({"success": True, "specializations": specs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/options', methods=['GET'])
def get_options():
    """Get all filter options"""
    try:
        districts = sorted(df['district'].unique().tolist())
        thanas = sorted(df['thana'].unique().tolist())
        specs = sorted(le_spec.classes_.tolist())
        
        return jsonify({
            "success": True,
            "options": {
                "districts": districts,
                "thanas": thanas,
                "specializations": specs
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/recommendations', methods=['POST'])
def get_doctor_recommendations():
    """Get doctor recommendations - MAIN ENDPOINT"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['district', 'thana', 'specialization', 'max_fee', 'online', 'emergency']
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing: {field}"}), 400
        
        top_n = data.get('top_n', 5)
        result = get_recommendations(data, top_n)
        
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🏥 DOCTOR RECOMMENDATION API - RUNNING")
    print("="*80)
    print("\n📍 API Base URL: http://localhost:5000/api")
    print("\n✅ All systems ready!")
    print("="*80 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0', use_reloader=False)
