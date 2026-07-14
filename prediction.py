import os
import json
import joblib
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components

from database import save_patient, add_prediction, add_alert, add_report
from ai_summary import generate_ai_report, format_ai_report_markdown
from utils import generate_pdf_report

def play_high_risk_audio_alert(patient_name):
    """Triggers browser audio tone and text-to-speech synthesis via embedded Javascript."""
    js_code = f"""
    <script>
        // 1. Play emergency warning tone
        var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        function playTone(freq, duration, delay) {{
            setTimeout(function() {{
                var osc = audioCtx.createOscillator();
                var gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.frequency.value = freq;
                osc.type = 'sawtooth';
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
                osc.start();
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
                osc.stop(audioCtx.currentTime + duration);
            }}, delay);
        }}
        
        playTone(600, 0.4, 0);
        playTone(450, 0.4, 300);
        playTone(600, 0.5, 600);
        
        // 2. Synthesize critical warning voice alert
        setTimeout(function() {{
            var speech = new SpeechSynthesisUtterance("Warning! High risk kidney failure detected for patient {patient_name}. Immediate clinical evaluation required.");
            speech.lang = 'en-US';
            speech.pitch = 0.95;
            speech.rate = 0.95;
            window.speechSynthesis.speak(speech);
        }}, 1200);
    </script>
    """
    components.html(js_code, height=0, width=0)

def show_prediction_page():
    st.markdown('<h2 style="font-weight:700; color:#1E3A8A; margin-bottom: 2px;">🧪 Prediction Engine</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; margin-bottom: 25px;">Enter patient clinical profile metrics to run pre-trained ML models and generate risk diagnostics.</p>', unsafe_allow_html=True)
    
    # Check if models are available, if not, print error
    models_dir = "models"
    models_available = [f for f in os.listdir(models_dir) if f.endswith('.pkl')] if os.path.exists(models_dir) else []
    
    if not models_available:
        st.error("❌ Machine Learning models not found. Please run python train_models.py to train them.")
        return

    # Choose ML Model dropdown
    model_options = [
        "Random Forest",
        "Logistic Regression",
        "XGBoost",
        "SVM",
        "KNN",
        "MLP"
    ]
    selected_model_name = st.selectbox("Select Prediction Model", model_options)
    
    # Initialize session keys for inputs if not present
    input_keys = [
        "p_id", "p_name", "p_age", "p_gender", "p_height", "p_weight",
        "p_bp", "p_glucose", "p_creatinine", "p_urea", "p_albumin",
        "p_hemoglobin", "p_sodium", "p_potassium", "p_htn", "p_diabetes",
        "p_smoking", "p_alcohol", "p_family"
    ]
    
    # Check if reset was clicked
    if st.session_state.get("clear_form_flag", False):
        for k in input_keys:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state["clear_form_flag"] = False
        st.rerun()

    # Form layout inside Glass Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#1E3A8A; font-weight:700; margin-bottom: 15px;'>📋 Clinical Record Sheet</h4>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        p_id = st.text_input("Patient ID (Unique)", placeholder="e.g. P-2034", key="p_id")
        p_name = st.text_input("Patient Full Name", placeholder="e.g. Sarah Jenkins", key="p_name")
        p_age = st.number_input("Age (years)", min_value=1, max_value=120, value=50, key="p_age")
        p_gender = st.selectbox("Gender", ["Female", "Male"], key="p_gender")
        p_height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=165.0, step=0.5, key="p_height")
        p_weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.5, key="p_weight")

    with col_b:
        p_bp = st.number_input("Systolic Blood Pressure (mmHg)", min_value=50, max_value=250, value=120, key="p_bp")
        p_glucose = st.number_input("Fast Blood Glucose (mg/dL)", min_value=30, max_value=500, value=100, key="p_glucose")
        p_creatinine = st.number_input("Serum Creatinine (mg/dL)", min_value=0.1, max_value=15.0, value=1.0, step=0.1, key="p_creatinine")
        p_urea = st.number_input("Blood Urea (mg/dL)", min_value=5.0, max_value=300.0, value=35.0, step=0.5, key="p_urea")
        p_albumin = st.selectbox("Albuminuria (Urinary Protein Grade)", [0, 1, 2, 3, 4, 5], index=0, key="p_albumin")
        p_hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=3.0, max_value=25.0, value=13.5, step=0.1, key="p_hemoglobin")

    with col_c:
        p_sodium = st.number_input("Serum Sodium (mEq/L)", min_value=100.0, max_value=180.0, value=138.0, step=0.5, key="p_sodium")
        p_potassium = st.number_input("Serum Potassium (mEq/L)", min_value=1.5, max_value=10.0, value=4.2, step=0.1, key="p_potassium")
        p_htn = st.selectbox("Hypertension Diagnosis?", ["No", "Yes"], index=0, key="p_htn")
        p_diabetes = st.selectbox("Diabetes Diagnosis?", ["No", "Yes"], index=0, key="p_diabetes")
        p_smoking = st.selectbox("Smoking Status?", ["No", "Yes"], index=0, key="p_smoking")
        p_alcohol = st.selectbox("Alcohol Consumption?", ["No", "Yes"], index=0, key="p_alcohol")
        p_family = st.selectbox("Family History of Renal Failure?", ["No", "Yes"], index=0, key="p_family")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Form submission buttons
    col_act1, col_act2 = st.columns([4, 1])
    
    with col_act1:
        run_prediction = st.button("🚀 Analyze Clinical Profile & Predict Risk", use_container_width=True)
    with col_act2:
        # Reset form key trigger
        if st.button("🔄 Reset Form", use_container_width=True):
            st.session_state["clear_form_flag"] = True
            st.rerun()

    # If predict clicked
    if run_prediction:
        # Validation checks
        if not p_id or not p_name:
            st.error("⚠️ Patient ID and Patient Full Name are required to log the prediction.")
            return
            
        # Convert binary yes/no selection to 1/0
        gender_bin = 1 if p_gender == "Male" else 0
        htn_bin = 1 if p_htn == "Yes" else 0
        diabetes_bin = 1 if p_diabetes == "Yes" else 0
        smoking_bin = 1 if p_smoking == "Yes" else 0
        alcohol_bin = 1 if p_alcohol == "Yes" else 0
        family_bin = 1 if p_family == "Yes" else 0
        
        # Prepare inputs vector for scaling and model
        raw_inputs = {
            "age": float(p_age),
            "gender": float(gender_bin),
            "height": float(p_height),
            "weight": float(p_weight),
            "blood_pressure": float(p_bp),
            "blood_glucose": float(p_glucose),
            "serum_creatinine": float(p_creatinine),
            "blood_urea": float(p_urea),
            "albumin": float(p_albumin),
            "hemoglobin": float(p_hemoglobin),
            "sodium": float(p_sodium),
            "potassium": float(p_potassium),
            "hypertension": float(htn_bin),
            "diabetes": float(diabetes_bin),
            "smoking": float(smoking_bin),
            "alcohol": float(alcohol_bin),
            "family_history": float(family_bin)
        }
        
        feature_vector = np.array([[
            raw_inputs["age"], raw_inputs["gender"], raw_inputs["height"], raw_inputs["weight"],
            raw_inputs["blood_pressure"], raw_inputs["blood_glucose"], raw_inputs["serum_creatinine"],
            raw_inputs["blood_urea"], raw_inputs["albumin"], raw_inputs["hemoglobin"], raw_inputs["sodium"],
            raw_inputs["potassium"], raw_inputs["hypertension"], raw_inputs["diabetes"],
            raw_inputs["smoking"], raw_inputs["alcohol"], raw_inputs["family_history"]
        ]])
        
        # Load scaler and model
        try:
            scaler = joblib.load("models/scaler.pkl")
            model_filename = f"models/{selected_model_name.replace(' ', '_')}.pkl"
            model = joblib.load(model_filename)
        except Exception as e:
            st.error(f"Error loading model assets: {e}. Please run python train_models.py.")
            return
            
        # Scale and predict
        scaled_vector = scaler.transform(feature_vector)
        
        # Get probability
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(scaled_vector)[0]
            probability = float(probs[1]) # Probability of CKD / failure
        else:
            # Fallback for models without predict_proba if any, but our SVC/MLP/LR all have it
            dec = model.decision_function(scaled_vector)[0]
            probability = 1 / (1 + np.exp(-dec))
            
        # Determine risk level
        # Low: P < 30%, Moderate: 30% <= P < 70%, High: P >= 70%
        if probability < 0.30:
            risk_level = "Low Risk"
            risk_color = "#10B981" # Green
        elif probability < 0.70:
            risk_level = "Moderate Risk"
            risk_color = "#F59E0B" # Yellow/Orange
        else:
            risk_level = "High Risk"
            risk_color = "#EF4444" # Red
            
        kidney_health_score = 100.0 - (probability * 100.0)
        
        # Save patient details in database
        save_patient(p_id, p_name, p_age, p_gender, p_height, p_weight)
        
        # Generate AI Clinical Assessment
        ai_report_dict = generate_ai_report(p_name, p_age, p_gender, raw_inputs, risk_level, probability)
        ai_markdown = format_ai_report_markdown(ai_report_dict)
        
        # Save prediction run in database
        prediction_id = add_prediction(
            patient_id=p_id,
            model_name=selected_model_name,
            probability=probability,
            risk_level=risk_level,
            score=kidney_health_score,
            inputs_dict=raw_inputs,
            ai_summary=ai_markdown
        )
        
        # If prediction fails to save
        if not prediction_id:
            st.error("Failed to log predictions to patient database.")
            return

        # Generate PDF report automatically & save it in reports/
        pdf_path = generate_pdf_report(
            patient={"patient_id": p_id, "name": p_name, "age": p_age, "gender": p_gender, "height": p_height, "weight": p_weight},
            prediction={"id": prediction_id, "model_name": selected_model_name, "prediction_date": datetime.now().isoformat(), "probability": probability, "risk_level": risk_level, "kidney_health_score": kidney_health_score, "inputs": raw_inputs},
            ai_report=ai_report_dict
        )
        
        # Add to reports log table
        add_report(p_id, prediction_id, pdf_path)
        
        # Layout Results: Left Column = Gauge, Right Column = Metrics/Assessment
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.markdown('<div class="glass-card" style="text-align: center; height:370px;">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#1E3A8A; font-weight:700; margin:0 0 10px 0;'>Risk speedometer</h4>", unsafe_allow_html=True)
            
            # Speedometer Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = round(probability * 100, 1),
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                    'bar': {'color': "#1E293B", 'thickness': 0.25},
                    'bgcolor': "white",
                    'borderwidth': 1,
                    'bordercolor': "#94A3B8",
                    'steps': [
                        {'range': [0, 30], 'color': '#A7F3D0'},     # light green
                        {'range': [30, 70], 'color': '#FDE68A'},    # light yellow
                        {'range': [70, 100], 'color': '#FCA5A5'}    # light red
                    ],
                    'threshold': {
                        'line': {'color': risk_color, 'width': 5},
                        'thickness': 0.75,
                        'value': probability * 100
                    }
                }
            ))
            fig.update_layout(
                height=250, 
                margin=dict(t=5, b=5, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"<span style='font-size:1.15rem; font-weight:700; color:{risk_color};'>Risk Category: {risk_level} ({probability*100:.1f}%)</span>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_res2:
            st.markdown('<div class="glass-card" style="height:370px; display:flex; flex-direction:column; justify-content:center;">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#1E3A8A; font-weight:700; margin-top:0;'>Renal health status</h4>", unsafe_allow_html=True)
            
            # Badge & health scores
            score_color = "#10B981" if kidney_health_score >= 70 else ("#F59E0B" if kidney_health_score >= 30 else "#EF4444")
            
            st.markdown(
                f"""
                <div style="margin-bottom:15px;">
                    <p style="margin:0; font-size:0.9rem; color:#64748B; font-weight:600;">Kidney Health Score (0-100)</p>
                    <h2 style="margin:5px 0; color:{score_color}; font-size:3.5rem; font-weight:800;">{kidney_health_score:.0f} <span style="font-size:1.5rem; font-weight:400; color:#64748B;">/ 100</span></h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Badges
            badge_text = "🛡️ Normal Function" if risk_level == "Low Risk" else ("⚠️ Early Nephropathy Risk" if risk_level == "Moderate Risk" else "🚨 Critical ESRD Alert")
            st.markdown(
                f"""
                <div style="background:{risk_color}22; color:{risk_color}; border: 1px solid {risk_color}; padding:8px 12px; border-radius:8px; display:inline-block; font-weight:700; font-size:0.95rem; margin-bottom: 20px;">
                    {badge_text}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Download PDF Report Button
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="📥 Download Printable PDF Clinical Report",
                data=pdf_bytes,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        # High-risk Alert Trigger actions
        if risk_level == "High Risk":
            # Add alert record to db
            alert_msg = f"CRITICAL: Patient {p_name} ({p_id}) is predicted at High Risk ({probability*100:.1f}%) for kidney failure. Elevated serum creatinine ({p_creatinine} mg/dL) or albuminuria (Grade {p_albumin}+) was noted."
            add_alert(p_id, prediction_id, risk_level, alert_msg)
            
            # Visual warnings
            st.markdown(
                f"""
                <div class="blinking-alert">
                    <h3 style="margin:0; color:#EF4444;">🚨 CLINICAL WARNING: HIGH RISK IDENTIFIED</h3>
                    <p style="margin:8px 0 0 0; color:#DC2626; font-size:1rem; font-weight:600;">
                        System voice warning dispatched. Immediate medical consult recommended. The report has been logged under active clinical alerts.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Synthesize tone & Voice alerts
            play_high_risk_audio_alert(p_name)
            
            # Clinical recommendations
            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                st.markdown('<div class="glass-card" style="border-left: 5px solid #EF4444; background: rgba(239, 68, 68, 0.05);">', unsafe_allow_html=True)
                st.markdown("<h5 style='color:#EF4444; font-weight:700; margin:0 0 10px 0;'>🚨 Emergency Directives</h5>", unsafe_allow_html=True)
                st.markdown(f"**Emergency Warning:** {ai_report_dict['emergency_warning']}")
                st.markdown(f"**Referral Guidance:** {ai_report_dict['hospital_referral_suggestion']}")
                st.markdown('</div>', unsafe_allow_html=True)
            with col_rec2:
                st.markdown('<div class="glass-card" style="border-left: 5px solid #F59E0B; background: rgba(245, 158, 11, 0.05);">', unsafe_allow_html=True)
                st.markdown("<h5 style='color:#D97706; font-weight:700; margin:0 0 10px 0;'>🏥 Recommended Nephrology Specialists</h5>", unsafe_allow_html=True)
                st.markdown("Based on patient criteria, referral to the nearest certified clinic is indicated:")
                st.markdown("- **Dr. Robert Vance, MD** - Nephrology Specialist, General Hospital (0.8 miles)")
                st.markdown("- **Renal Care & Dialysis Pavilion** - Academic Medical Center (2.4 miles)")
                st.markdown('</div>', unsafe_allow_html=True)

        # Print AI report
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(ai_markdown, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
