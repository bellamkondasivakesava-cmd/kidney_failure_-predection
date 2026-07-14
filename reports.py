import os
import pandas as pd
import streamlit as st
from database import get_all_predictions, get_reports_for_patient

def show_reports_page():
    st.markdown('<h2 style="font-weight:700; color:#1E3A8A; margin-bottom: 2px;">📂 Clinical Reports</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; margin-bottom: 25px;">Compile clinical data, download official PDF documents, and compare patient progress charts.</p>', unsafe_allow_html=True)
    
    preds = get_all_predictions()
    
    if not preds:
        st.info("No prediction data available. Generate a prediction run first.")
        return
        
    df = pd.DataFrame(preds)
    
    # Select Patient
    patient_ids = df['patient_id'].unique()
    patient_options = {}
    for pid in patient_ids:
        # Get patient name
        p_name = df[df['patient_id'] == pid]['patient_name'].values[0]
        patient_options[pid] = f"{p_name} ({pid})"
        
    selected_pid = st.selectbox(
        "Select Patient Profile", 
        options=list(patient_options.keys()), 
        format_func=lambda x: patient_options[x]
    )
    
    # Filter predictions for selected patient
    patient_preds = [p for p in preds if p['patient_id'] == selected_pid]
    patient_preds = sorted(patient_preds, key=lambda x: x['prediction_date'], reverse=True)
    
    st.write(f"Found **{len(patient_preds)}** historical records for this patient.")
    
    # Tab layout: Single Report View vs Progress Comparison
    tab_single, tab_compare = st.tabs(["👁️ View & Download Reports", "🔄 Compare Reports (Progress Tracking)"])
    
    with tab_single:
        if not patient_preds:
            st.warning("No records found.")
        else:
            # Dropdown of dates
            run_options = {p['id']: f"{p['prediction_date'][:16].replace('T', ' ')} — {p['risk_level']} ({p['model_name']})" for p in patient_preds}
            selected_run_id = st.selectbox("Select Assessment Run", options=list(run_options.keys()), format_func=lambda x: run_options[x])
            
            # Find selected run dict
            run = next(p for p in patient_preds if p['id'] == selected_run_id)
            
            col_d1, col_d2 = st.columns([2, 1])
            with col_d1:
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding:15px; margin-bottom: 15px;">
                        <h4 style="margin:0 0 10px 0; color:#1E3A8A;">Run Details</h4>
                        <table style="width:100%; border-collapse:collapse; font-size:0.95rem;">
                            <tr><td style="padding:4px; font-weight:600;">Prediction Date:</td><td>{run['prediction_date'][:16].replace('T', ' ')}</td></tr>
                            <tr><td style="padding:4px; font-weight:600;">Model Employed:</td><td>{run['model_name']}</td></tr>
                            <tr><td style="padding:4px; font-weight:600;">Risk Classification:</td><td><b>{run['risk_level']}</b></td></tr>
                            <tr><td style="padding:4px; font-weight:600;">Risk Probability:</td><td>{run['probability']*100:.1f}%</td></tr>
                            <tr><td style="padding:4px; font-weight:600;">Kidney Health Score:</td><td><b>{run['kidney_health_score']:.0f}/100</b></td></tr>
                        </table>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col_d2:
                st.markdown('<div class="glass-card" style="padding:15px; text-align:center; height:180px; display:flex; flex-direction:column; justify-content:center;">', unsafe_allow_html=True)
                pdf_filename = f"reports/nephroguard_{selected_pid}_{selected_run_id}.pdf"
                if os.path.exists(pdf_filename):
                    with open(pdf_filename, "rb") as f:
                        pdf_data = f.read()
                    st.download_button(
                        label="📥 Download PDF Document",
                        data=pdf_data,
                        file_name=os.path.basename(pdf_filename),
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.write("*PDF file missing.*")
                st.markdown('</div>', unsafe_allow_html=True)
                
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(run['ai_summary'], unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_compare:
        if len(patient_preds) < 2:
            st.info("At least two prediction runs are required to perform a comparison analysis. This patient currently has only one run.")
        else:
            st.write("Select two assessments to evaluate changes in clinical metrics side-by-side:")
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                run1_id = st.selectbox("Select Baseline Report (Older)", options=list(run_options.keys()), format_func=lambda x: run_options[x], index=len(patient_preds)-1)
            with col_c2:
                run2_id = st.selectbox("Select Comparison Report (Newer)", options=list(run_options.keys()), format_func=lambda x: run_options[x], index=0)
                
            if run1_id == run2_id:
                st.warning("Please select two distinct reports to perform comparison.")
            else:
                run1 = next(p for p in patient_preds if p['id'] == run1_id)
                run2 = next(p for p in patient_preds if p['id'] == run2_id)
                
                # Side by side visual metrics
                col_m1, col_m2 = st.columns(2)
                
                with col_m1:
                    st.markdown(
                        f"""
                        <div class="glass-card" style="border-left: 5px solid #2563EB;">
                            <h5>Baseline Run ({run1['prediction_date'][:10]})</h5>
                            <p style="margin:0; font-size:0.85rem; color:#64748B;">Kidney Health Score</p>
                            <h3 style="color:#2563EB; font-weight:800; font-size:2rem; margin:5px 0;">{run1['kidney_health_score']:.0f}/100</h3>
                            <span style="font-weight:600;">Risk: {run1['risk_level']}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with col_m2:
                    # Compare and show delta arrow
                    diff = run2['kidney_health_score'] - run1['kidney_health_score']
                    if diff > 0:
                        delta_str = f"<span style='color:#10B981; font-weight:bold;'>▲ +{diff:.1f} (Improvement)</span>"
                    elif diff < 0:
                        delta_str = f"<span style='color:#EF4444; font-weight:bold;'>▼ {diff:.1f} (Decline)</span>"
                    else:
                        delta_str = "<span style='color:#64748B; font-weight:bold;'>● No Change</span>"
                        
                    st.markdown(
                        f"""
                        <div class="glass-card" style="border-left: 5px solid #10B981;">
                            <h5>Comparison Run ({run2['prediction_date'][:10]})</h5>
                            <p style="margin:0; font-size:0.85rem; color:#64748B;">Kidney Health Score</p>
                            <h3 style="color:#10B981; font-weight:800; font-size:2rem; margin:5px 0;">{run2['kidney_health_score']:.0f}/100</h3>
                            <span>Delta: {delta_str}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Key clinical metric comparisons
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("<h4 style='color:#1E3A8A; font-weight:700; margin-bottom: 10px;'>🔬 Clinical Metric Tracking Table</h4>", unsafe_allow_html=True)
                
                inp1 = run1['inputs']
                inp2 = run2['inputs']
                
                # Assemble comparisons rows
                comparison_rows = [
                    ("Serum Creatinine (mg/dL)", inp1.get('serum_creatinine', 1.0), inp2.get('serum_creatinine', 1.0)),
                    ("Blood Urea (mg/dL)", inp1.get('blood_urea', 40.0), inp2.get('blood_urea', 40.0)),
                    ("Systolic Blood Pressure (mmHg)", inp1.get('blood_pressure', 120.0), inp2.get('blood_pressure', 120.0)),
                    ("Blood Glucose (mg/dL)", inp1.get('blood_glucose', 100.0), inp2.get('blood_glucose', 100.0)),
                    ("Hemoglobin (g/dL)", inp1.get('hemoglobin', 13.5), inp2.get('hemoglobin', 13.5)),
                    ("Albuminuria Grade", f"Grade {inp1.get('albumin', 0)}+", f"Grade {inp2.get('albumin', 0)}+"),
                    ("Serum Sodium (mEq/L)", inp1.get('sodium', 138.0), inp2.get('sodium', 138.0)),
                    ("Serum Potassium (mEq/L)", inp1.get('potassium', 4.2), inp2.get('potassium', 4.2))
                ]
                
                comp_data = []
                for label, v1, v2 in comparison_rows:
                    # Calculate difference if they are numbers
                    if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                        d = v2 - v1
                        if d > 0:
                            change = f"+{d:.2f}"
                        elif d < 0:
                            change = f"{d:.2f}"
                        else:
                            change = "0.00"
                    else:
                        change = "N/A"
                        
                    comp_data.append({
                        "Clinical Metric": label,
                        "Baseline Run Value": v1,
                        "Comparison Run Value": v2,
                        "Delta (Change)": change
                    })
                    
                st.table(pd.DataFrame(comp_data))
                st.markdown('</div>', unsafe_allow_html=True)
