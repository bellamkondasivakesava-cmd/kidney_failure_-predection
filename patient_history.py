import os
import pandas as pd
import streamlit as st
from datetime import datetime
from database import get_all_predictions, delete_prediction, save_patient

def show_history_page():
    st.markdown('<h2 style="font-weight:700; color:#1E3A8A; margin-bottom: 2px;">📋 Patient History & Records</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; margin-bottom: 25px;">Search, edit, filter, and review historical risk assessments and clinical files.</p>', unsafe_allow_html=True)
    
    preds = get_all_predictions()
    
    if not preds:
        st.info("No historical assessment records found. Generate a prediction to begin.")
        return
        
    # Search and Filter Widgets
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("🔍 Search & Filter Tools")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        search_query = st.text_input("Fuzzy Search (Name / Patient ID)", placeholder="Enter name or ID...").lower().strip()
    with col_f2:
        filter_risk = st.selectbox("Filter by Risk Level", ["All", "Low Risk", "Moderate Risk", "High Risk"])
    with col_f3:
        filter_model = st.selectbox("Filter by Model Name", ["All", "Random Forest", "Logistic Regression", "XGBoost", "SVM", "KNN", "MLP"])
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter operations
    filtered_preds = []
    for pr in preds:
        # Check text search
        p_id = pr['patient_id'].lower()
        p_name = pr['patient_name'].lower()
        if search_query and (search_query not in p_id and search_query not in p_name):
            continue
            
        # Check risk level
        if filter_risk != "All" and pr['risk_level'] != filter_risk:
            continue
            
        # Check model name
        if filter_model != "All" and pr['model_name'] != filter_model:
            continue
            
        filtered_preds.append(pr)
        
    # Export CSV Option
    if filtered_preds:
        export_data = []
        for pr in filtered_preds:
            row = {
                "Prediction_ID": pr['id'],
                "Patient_ID": pr['patient_id'],
                "Patient_Name": pr['patient_name'],
                "Age": pr['patient_age'],
                "Gender": pr['patient_gender'],
                "Assessed_Date": pr['prediction_date'],
                "Model_Used": pr['model_name'],
                "Risk_Level": pr['risk_level'],
                "CKD_Probability": round(pr['probability'], 4),
                "Health_Score": round(pr['kidney_health_score'], 1)
            }
            # Add clinical inputs
            for k, v in pr['inputs'].items():
                row[f"Input_{k}"] = v
            export_data.append(row)
            
        export_df = pd.DataFrame(export_data)
        csv_bytes = export_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Export Filtered Records to CSV",
            data=csv_bytes,
            file_name=f"nephroguard_records_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.write("") # Spacer
        
    else:
        st.warning("No records match your selected search and filter criteria.")
        return

    # Render Patient Cards
    for pr in filtered_preds:
        pid = pr['patient_id']
        pname = pr['patient_name']
        risk = pr['risk_level']
        date_str = pr['prediction_date'][:16].replace('T', ' ')
        model = pr['model_name']
        score = pr['kidney_health_score']
        prob = pr['probability']
        pred_id = pr['id']
        
        risk_color = {
            "Low Risk": "🟢",
            "Moderate Risk": "🟡",
            "High Risk": "🔴"
        }.get(risk, "")
        
        # Expander Header
        header_label = f"{risk_color} [{pid}] {pname} — {risk} ({prob*100:.1f}%) | {date_str} ({model})"
        
        with st.expander(header_label):
            st.markdown(f"#### Patient File & Diagnostics ID: `RUN-{pred_id:05d}`")
            
            tab_view, tab_edit = st.tabs(["👁️ View Details & Recommendations", "✏️ Edit Patient Profile"])
            
            with tab_view:
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    st.write("**Patient Demographics:**")
                    st.write(f"- **Age / Gender:** {pr['patient_age']} years / {pr['patient_gender']}")
                    st.write(f"- **Height / Weight:** {pr['inputs'].get('height')} cm / {pr['inputs'].get('weight')} kg")
                    st.write(f"- **Kidney Health Score:** `{score:.1f}/100`")
                    
                with col_i2:
                    st.write("**Clinical Lab Results:**")
                    inp = pr['inputs']
                    st.write(f"- **Blood Pressure:** {inp.get('blood_pressure')} mmHg")
                    st.write(f"- **Serum Creatinine:** {inp.get('serum_creatinine')} mg/dL")
                    st.write(f"- **Blood Urea:** {inp.get('blood_urea')} mg/dL")
                    st.write(f"- **Albuminuria Grade:** Grade {inp.get('albumin')}+")
                    st.write(f"- **Hemoglobin:** {inp.get('hemoglobin')} g/dL")
                    st.write(f"- **Electrolytes:** Sodium {inp.get('sodium')} | Potassium {inp.get('potassium')}")
                    
                # PDF report download
                pdf_filename = f"reports/nephroguard_{pid}_{pred_id}.pdf"
                if os.path.exists(pdf_filename):
                    with open(pdf_filename, "rb") as f:
                        pdf_data = f.read()
                    st.download_button(
                        label="📥 Download PDF Clinical Report",
                        data=pdf_data,
                        file_name=os.path.basename(pdf_filename),
                        mime="application/pdf",
                        key=f"dl_pdf_{pred_id}"
                    )
                else:
                    st.write("*PDF clinical document was deleted or not generated.*")
                    
                # Print the saved AI summary report in markdown
                st.markdown("---")
                st.write(pr['ai_summary'])
                
                # Delete Run Button
                st.markdown("---")
                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                if st.button("🗑️ Delete Assessment Record", key=f"del_rec_{pred_id}"):
                    if delete_prediction(pred_id):
                        st.success("Record deleted successfully.")
                        st.rerun()
                    else:
                        st.error("Failed to delete record.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with tab_edit:
                st.write("Modify patient demographics in the databases. (Note: This updates patient records, but does not alter past prediction inputs themselves.)")
                
                with st.form(f"edit_patient_form_{pred_id}"):
                    new_name = st.text_input("Patient Full Name", value=pname)
                    new_age = st.number_input("Age (years)", min_value=1, max_value=120, value=int(pr['patient_age']))
                    new_gender = st.selectbox("Gender", ["Female", "Male"], index=0 if pr['patient_gender'] == "Female" else 1)
                    new_height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=float(pr['inputs'].get('height', 165.0)))
                    new_weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=float(pr['inputs'].get('weight', 70.0)))
                    
                    saved = st.form_submit_button("💾 Save Profile Updates")
                    if saved:
                        if new_name.strip():
                            success = save_patient(
                                patient_id=pid,
                                name=new_name.strip(),
                                age=new_age,
                                gender=new_gender,
                                height=new_height,
                                weight=new_weight
                            )
                            if success:
                                st.success("Patient profile updated successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to update profile.")
                        else:
                            st.error("Name cannot be empty.")
