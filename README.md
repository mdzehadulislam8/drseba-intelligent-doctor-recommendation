# 🏥 Doctor Recommendation System - AI-Powered

> **An end-to-end Machine Learning platform for intelligent doctor recommendations based on location, specialization, fees, and service availability.**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![CatBoost](https://img.shields.io/badge/CatBoost-ML-orange.svg)](https://catboost.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📊 Project Overview

This is a **production-ready ML system** that recommends doctors based on:
- 📍 Geographic location (District/Thana)
- 👨‍⚕️ Medical specialization
- 💰 Consultation fees
- 🏥 Hospital facilities (Online/Emergency services)

**Real Dataset:** 500+ verified doctors across Bangladesh  
**AI Engine:** CatBoost classifier with 99.63% accuracy  
**Architecture:** Django REST API + Server-side rendering

---

## 🎯 Key Features

✅ **AI-Powered Recommendations** — CatBoost model with 99.63% R² Score  
✅ **Multiple Models Trained** — CatBoost + Gradient Boosting (98.79%) + XGBoost + AdaBoost  
✅ **Real-Time Search** — Filter from 500+ doctor database  
✅ **Dual Interface** — Web UI + REST API for developers  
✅ **Network API** — Share API across team on same network  
✅ **Production Ready** — Django best practices, comprehensive error handling  
✅ **Full Documentation** — API guide, architecture, and examples  

---

## 📈 Model Accuracy Comparison

Comprehensive evaluation of 4 state-of-the-art boosting algorithms:

| Model | RMSE | R² Score | Accuracy | Status |
|-------|------|----------|----------|--------|
| **CatBoost** 🏆 | **0.0126** | **0.9963** | **99.63%** | ✅ **BEST** |
| Gradient Boosting 🌟 | **0.0227** | **0.9879** | **98.79%** | ✅ **EXCELLENT** |
| XGBoost | 0.0235 | 0.9870 | 98.70% | ✅ Good |
| AdaBoost | 0.0793 | 0.8520 | 85.20% | ⚠️ Acceptable |

### 🎯 Model Selection Rationale

**CatBoost (Selected) - 99.63% Accuracy** 🏆
- ✅ Native handling of categorical features (District, Thana, Specialization)
- ✅ Lowest RMSE (0.0126) — most precise predictions
- ✅ Highest R² Score — 99.63% variance explained
- ✅ Built-in overfitting protection
- ✅ Excellent with imbalanced/categorical data
- ✅ Faster training and inference

**Why Not Gradient Boosting (98.79%)?** 🌟
- Very close second (only 0.84% difference from CatBoost)
- Requires manual categorical encoding
- Slightly higher RMSE (0.0227 vs 0.0126)
- Still excellent for production use

**Performance Insights:**
- CatBoost's native categorical handling gives ~1% edge
- Both CatBoost & GB have >98% accuracy (both production-viable)
- XGBoost (98.70%) and AdaBoost (85.20%) also competitive but less optimal

---

## 📸 User Interface

### Input Page
![Input Interface](https://drive.google.com/uc?export=view&id=1OVoBvt2csRNjh2RqzHcuzMvtI9NjpcpE)

Fill in your requirements:
- Select District (Dhaka, Chittagong, etc.)
- Choose Thana/Area
- Select Medical Specialization
- Set Maximum Consultation Fee
- Optional: Filter by Online/Emergency services

### Output Page
![Output Results](https://drive.google.com/uc?export=view&id=1KD2jkHPG8esA16JSQ3nH67Cn0HHeXueZ)

Get recommendations ranked by AI quality score:
- Doctor name and specialization
- Rating and experience
- Consultation fees
- Hospital details
- AI quality prediction (Excellent/Good/Fair)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Web Browser / Client                    │
│         (Input page → Submit → Output results)           │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Request
                     ↓
┌─────────────────────────────────────────────────────────┐
│              Django Backend (Port 7777)                  │
├─────────────────────────────────────────────────────────┤
│ • Web UI: demo_ui/ (Server-side rendered templates)    │
│ • API Endpoints: /api/recommendations, /api/health etc. │
│ • Business Logic: recommender/views.py                  │
│ • Routing: drseba_platform/urls.py                      │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   ┌────────┐  ┌──────────┐  ┌──────────┐
   │ CatBoost│  │ Pandas   │  │ Excel    │
   │ ML Model│  │ Data Proc│  │ Database │
   └────────┘  └──────────┘  └──────────┘
```

---

## 📁 Repository Structure

```
model/
├── drseba_platform/                    # Django Project Configuration
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # URL routing
│   └── wsgi.py                        # WSGI application
│
├── recommender/                        # Django App (Main Logic)
│   ├── views.py                       # API endpoints + ML logic
│   ├── urls.py                        # App routing
│   ├── management/commands/
│   │   └── runnetwork.py              # Custom Django command
│   └── apps.py
│
├── demo_ui/                            # Frontend
│   ├── index.html                     # Django template
│   └── style.css                      # Styling
│
├── data/                               # Dataset
│   └── Dr.Seba_500_Organized_Final.xlsx  # 500+ doctors
│
├── models/                             # ML Models
│   └── doctor_ai_full_package.pkl     # CatBoost (99.63% R²)
│
├── legacy/                             # Archive (Old Flask version)
│   ├── doctor_api.py                  # Flask API v1
│   └── run_frontend.py                # Flask server v1
│
├── api/                                # Duplicate (Not used)
│
├── manage.py                           # Django entry point
├── requirements.txt                    # Python dependencies
├── HOW_TO_RUN.md                       # Setup guide
├── DEVELOPER_API_GUIDE.md              # API documentation
└── README.md                           # This file
```

---

## 🚀 Quick Start

### 1️⃣ Installation

```bash
# Clone repository
git clone <repository-url>
cd model

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Run Server

**Option A: Django Custom Command (Recommended)**
```bash
python manage.py runnetwork
```

**Output:**
```
========================================
  Doctor Recommendation API Server
========================================
✓ Local Network IP: 192.168.10.23
✓ Port: 7777

📍 Access URLs:
   Network: http://192.168.10.23:7777
   Localhost: http://127.0.0.1:7777
```

**Option B: Manual**
```bash
python manage.py runserver 0.0.0.0:7777
```

### 3️⃣ Access Application

**🌐 Web UI:**
```
http://192.168.10.23:7777/
```

**📡 API Root:**
```
http://192.168.10.23:7777/api/
```

---

## 📚 API Documentation

### Health Check
```bash
GET /api/health
```
Response:
```json
{"status": "healthy"}
```

### Get All Options
```bash
GET /api/options
```
Response:
```json
{
  "success": true,
  "options": {
    "districts": ["Dhaka", "Chittagong", ...],
    "thanas": [...],
    "specializations": [...]
  }
}
```

### Get Thanas for District
```bash
GET /api/thanas/Dhaka
```

### Get Doctor Recommendations ⭐ (Main Endpoint)
```bash
POST /api/recommendations
Content-Type: application/json

{
  "district": "Dhaka",
  "thana": "Dhanmondi",
  "specialization": "Cardiology",
  "max_fee": 2000,
  "online": 1,
  "emergency": 0,
  "top_n": 5
}
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "doctors": [
    {
      "doctor_name": "Dr. Ahmed Khan",
      "specialization": "Cardiology",
      "rating_avg": 4.8,
      "experience_years": 12,
      "consultation_fees": 1500,
      "predicted_score": 1.8234,
      "hospital_name": "Apollo Hospital",
      "full_address": "Dhaka Medical Center, Dhanmondi"
    },
    ...
  ]
}
```

---

## 💻 Developer Integration

### Python Client
```python
import requests

response = requests.post(
    'http://192.168.10.23:7777/api/recommendations',
    json={
        "district": "Dhaka",
        "thana": "Dhanmondi",
        "specialization": "Cardiology",
        "max_fee": 2000,
        "online": 1,
        "emergency": 0,
        "top_n": 5
    }
)
doctors = response.json()['doctors']
for doc in doctors:
    print(f"{doc['doctor_name']} - Score: {doc['predicted_score']}")
```

### JavaScript Client
```javascript
const payload = {
  district: "Dhaka",
  thana: "Dhanmondi",
  specialization: "Cardiology",
  max_fee: 2000,
  online: 1,
  emergency: 0,
  top_n: 5
};

fetch('http://192.168.10.23:7777/api/recommendations', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload)
})
.then(r => r.json())
.then(data => console.log(data.doctors));
```

---

## 🔧 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Django 5.0 | Web framework & API |
| **ML Engine** | CatBoost | Doctor quality prediction |
| **Data Processing** | Pandas + NumPy | Feature engineering |
| **Encoding** | Scikit-learn | Categorical encoding |
| **Model Storage** | Pickle | Serialization |
| **Frontend** | HTML + CSS | User interface |
| **Template Engine** | Django Templates | Server-side rendering |
| **Database** | Excel (.xlsx) | 500+ doctor records |

---

## 📊 Model Training Details

**Dataset:** 500+ doctors from Bangladesh  
**Features:**
- Geographic: District, Thana
- Medical: Specialization (encoded)
- Financial: Consultation fees
- Operational: Online consultation, Emergency service
- Performance: Rating, Experience, Hospital type

**Target:** Quality Score (predicted by CatBoost)

**Best Practices:**
- LabelEncoder for categorical features
- Feature scaling where needed
- Cross-validation for robustness
- Hyperparameter tuning completed

---

## 🎓 Acknowledgments

### Mentor & Guidance
**Nusrat Jahan** — Data Science Trainer & Mentor
- Project conceptualization and ML methodology
- Model selection strategy (Why CatBoost?)
- Data science best practices
- Quality assurance and validation oversight

This project was developed under professional mentorship during an internship program focusing on applied machine learning and data-driven decision systems.

---

## 📝 Project Flow

1. **Data Collection** → 500+ verified doctor records across Bangladesh
2. **EDA & Preprocessing** → Handle missing values, encode categorical features
3. **Model Training** → 4 models compared:
   - ✅ CatBoost: **99.63% R²** (Selected)
   - ✅ Gradient Boosting: **98.79% R²**
   - ✅ XGBoost: 98.70% R²
   - ⚠️ AdaBoost: 85.20% R²
4. **Backend Integration** → Django REST API with CatBoost
5. **Frontend Development** → Server-side template rendering (No JavaScript)
6. **Testing & Deployment** → Network API ready for team integration

---

## 🔐 Security & Best Practices

✅ CSRF protection enabled  
✅ Input validation implemented  
✅ Error handling comprehensive  
✅ CORS enabled for team sharing  
✅ Django security middleware active  
✅ No hardcoded credentials  

---

## 📖 Additional Documentation

- **[HOW_TO_RUN.md](HOW_TO_RUN.md)** — Detailed setup & troubleshooting
- **[DEVELOPER_API_GUIDE.md](DEVELOPER_API_GUIDE.md)** — Complete API reference
- **[legacy/README.md](legacy/README.md)** — Old Flask v1 architecture

---

## 🌟 Key Metrics

| Metric | Value |
|--------|-------|
| **Best Model** (CatBoost) | **99.63% R²** |
| **Alternative** (Gradient Boosting) | **98.79% R²** |
| **Lowest RMSE** | 0.0126 |
| **Dataset Size** | 500+ doctors |
| **API Response Time** | < 100ms |
| **Supported Districts** | 10+ |
| **Medical Specializations** | 30+ |
| **Models Evaluated** | 4 (CatBoost, GB, XGBoost, AdaBoost) |

---

## 📋 Requirements

See `requirements.txt` for full list:
- Django 5.0+
- CatBoost 1.2+
- Pandas 2.0+
- Scikit-learn 1.3+
- NumPy 1.24+

---

## 📧 Support & Contact

For issues, questions, or collaboration:
- 📚 **API Issues**: Review **[DEVELOPER_API_GUIDE.md](DEVELOPER_API_GUIDE.md)** for API details
- 🚀 **Setup Issues**: Check **[HOW_TO_RUN.md](HOW_TO_RUN.md)** for setup issues
- 👤 **Mentor**: [Nusrat Jahan](https://github.com/Nusrat-96) — [nusratadiba88@gmail.com](mailto:nusratadiba88@gmail.com)

---

**Made with ❤️ for Dr.Seba Platform**  
*Last Updated: April 2026*
