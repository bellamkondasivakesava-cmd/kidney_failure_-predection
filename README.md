# NephroGuard AI - Intelligent Kidney Risk Alert System

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=bellamkondasivakesava-cmd/kidney_failure_-predection&branch=main&mainModule=app.py)

NephroGuard AI is a high-fidelity, professional healthcare web application designed to predict kidney failure risk using pre-trained Machine Learning models. Built using **Python and Streamlit**, it enables clinicians to register accounts, manage patients, run diagnostic simulations, trigger automated high-risk sirens, consult an AI expert chatbot, and download professional PDF clinical reports.

---

## Key Features

1. **🔒 Secure Authentication:** Hashed credentials utilizing `bcrypt` stored locally in an SQLite database (`users.db`).
2. **🧪 Multi-Model Clinical Classifier:** Runs patient variables against six different classifiers: Logistic Regression, Random Forest, XGBoost, SVM, KNN, and MLP Neural Networks.
3. **📊 Interactive Analytical Dashboard:** Features animated charts displaying risk counts, patient age/gender distributions, and historical trends built using Plotly.
4. **🔴 Real-time Siren & Alerts:** Triggers client-side browser warning beeps and Text-to-Speech voice warnings when a prediction falls into the **High Risk** category ($\ge 70\%$).
5. **🖨️ Professional PDF Document Generator:** Generates comprehensive PDF diagnostic records with hospital layouts, clinician signatures, and clinical findings using `ReportLab`.
6. **🔄 Side-by-side Progress Tracker:** Compares any two prediction reports side-by-side to track changes in serum creatinine, blood urea, and kidney health score over time.
7. **💬 AI Clinician Chat Assistant:** A kidney health specialist chatbot utilizing clinical templates to reply to dietary, hydration, lifestyle, and symptom queries without needing external keys.
8. **⚙️ Profile Preferences & Exports:** Offers password resets, dark mode layout toggle, and raw database exports (`.db` downloads) for clinical audit compliance.

---

## Directory Architecture

```
Kidney_AI_Agent/
├── app.py                   # Main layout and multi-page routing
├── login.py                 # Clinician login form with glassmorphism CSS
├── register.py              # User signup form with credential checks
├── dashboard.py             # Analytical home view with Plotly charts
├── prediction.py            # Patient inputs form, ML scoring, speedometers, & voice alert
├── reports.py               # PDF visualizer and side-by-side patient comparison
├── patient_history.py       # Patient database records (view, update, delete, CSV export)
├── settings.py              # Profile updates, dark theme, and database backup
│
├── database.py              # SQLite schemas and CRUD functions
├── auth.py                  # Hashing, password strength checks, signup checks
├── ai_summary.py            # AI report summaries and chatbot response logic
├── utils.py                 # Custom styling, PDF generator, and PIL asset creators
│
├── train_models.py          # Script to generate synthetic medical data & save ML models
│
├── models/                  # Stored classifier .pkl models
│   ├── Logistic_Regression.pkl
│   ├── Random_Forest.pkl
│   ├── XGBoost.pkl
│   ├── SVM.pkl
│   ├── KNN.pkl
│   ├── MLP.pkl
│   └── scaler.pkl
│
├── database/                # Local SQLite databases (created automatically)
│   ├── users.db
│   └── patients.db
│
├── reports/                 # Output PDF documents (created automatically)
└── requirements.txt         # Core dependencies
```

---

## Installation & Setup

Ensure Python 3.8+ is installed on your local system, then follow the instructions below:

### 1. Clone the project and navigate to the directory
```bash
cd kidney_failure_prediction
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Clinical Machine Learning Models
To generate the pre-trained `.pkl` files and `scaler.pkl` using synthetic medical data representing realistic clinical ranges, run the training pipeline script:
```bash
python train_models.py
```
This generates:
- Synthetic clinical logs representing 1,200 mock records.
- Balanced data scaling utilizing `StandardScaler`.
- Pickle models generated inside the `models/` directory.

### 4. Launch the Web Application
Launch the Streamlit portal server:
```bash
streamlit run app.py
```

---

## Clinical Input Parameters

To obtain a kidney failure prediction, the clinician enters **17 clinical attributes** representing key indicators:
* **Serum Creatinine (mg/dL):** Key waste product from muscles. Normal: 0.6 - 1.2 mg/dL. Elevated levels indicate renal filtering impairment.
* **Albuminuria Grade (0-5+):** Level of protein leaked in urine. Grade 1+ to 5+ indicates worsening filtration barrier damage.
* **Systolic Blood Pressure (mmHg):** High BP accelerates glomerular nephron scarring.
* **Fast Blood Glucose (mg/dL):** Elevated glucose represents diabetic nephropathy risks.
* **Blood Urea (mg/dL):** Measures nitrogenous waste. High levels indicate impaired urea excretion.
* **Hemoglobin (g/dL):** Low levels indicate potential anemia, secondary to erythropoietin hormone deficiency.
* **Serum Sodium & Potassium (mEq/L):** Tracks electrolyte balances (hyponatremia, hyperkalemia risk).
* **Hypertension / Diabetes Diagnoses:** Tracks underlying medical conditions driving CKD.
* **Smoking / Alcohol / Family History:** Visual lifestyle and genetics risk factors.

---

## Security & Medical Compliance Disclaimer

* **Hashed Passwords:** Passwords must be at least 8 characters long, contain an uppercase letter, lowercase letter, digit, and symbol. Hashed securely inside the database using the `bcrypt` library.
* **Education Use Only:** NephroGuard AI is designed as a demonstration helper for clinical workflows. It is trained on synthetic data and should not be used as a replacement for certified medical equipment or direct clinical diagnosis.
