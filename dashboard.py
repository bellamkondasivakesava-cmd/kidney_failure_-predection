import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from database import get_all_predictions, get_active_alerts

def show_dashboard_page():
    st.markdown('<h2 style="font-weight:700; color:#1E3A8A; margin-bottom: 2px;">📊 Clinical Dashboard</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; margin-bottom: 25px;">Real-time analytical view of kidney failure risk metrics and critical alerts.</p>', unsafe_allow_html=True)
    
    # Retrieve predictions and active alerts from DB
    preds = get_all_predictions()
    active_alerts = get_active_alerts()
    
    if not preds:
        st.info("No prediction data available. Please navigate to the Prediction Engine to add patients.")
        return

    # Convert predictions to a pandas DataFrame
    df = pd.DataFrame(preds)
    
    # Calculate Metrics
    total_patients = df['patient_id'].nunique()
    
    # Count of current risk categories based on the LATEST prediction for each patient
    df_latest = df.sort_values('prediction_date').groupby('patient_id').last().reset_index()
    
    high_risk_count = len(df_latest[df_latest['risk_level'] == 'High Risk'])
    mod_risk_count = len(df_latest[df_latest['risk_level'] == 'Moderate Risk'])
    low_risk_count = len(df_latest[df_latest['risk_level'] == 'Low Risk'])
    
    # Today's predictions count
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_preds_count = len(df[df['prediction_date'].str.startswith(today_str)])
    
    active_alerts_count = len(active_alerts)
    
    # Render Top Metric Cards in Columns
    st.markdown('<div style="margin-bottom: 10px;">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(
            f"""
            <div class="glass-card" style="padding:15px; text-align:center; height:130px; margin-bottom:10px;">
                <p style="margin:0; font-size:0.9rem; color:#64748B; font-weight:600;">Total Patients</p>
                <h3 style="margin:5px 0; color:#2563EB; font-size:2rem; font-weight:700;">{total_patients}</h3>
                <span style="font-size:0.75rem; color:#10B981;">● Registered</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"""
            <div class="glass-card" style="padding:15px; text-align:center; height:130px; margin-bottom:10px;">
                <p style="margin:0; font-size:0.9rem; color:#64748B; font-weight:600;">High Risk</p>
                <h3 style="margin:5px 0; color:#EF4444; font-size:2rem; font-weight:700;">{high_risk_count}</h3>
                <span style="font-size:0.75rem; color:#EF4444;">● Immediate Action</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col3:
        st.markdown(
            f"""
            <div class="glass-card" style="padding:15px; text-align:center; height:130px; margin-bottom:10px;">
                <p style="margin:0; font-size:0.9rem; color:#64748B; font-weight:600;">Moderate Risk</p>
                <h3 style="margin:5px 0; color:#F59E0B; font-size:2rem; font-weight:700;">{mod_risk_count}</h3>
                <span style="font-size:0.75rem; color:#F59E0B;">● Monitoring</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col4:
        st.markdown(
            f"""
            <div class="glass-card" style="padding:15px; text-align:center; height:130px; margin-bottom:10px;">
                <p style="margin:0; font-size:0.9rem; color:#64748B; font-weight:600;">Low Risk</p>
                <h3 style="margin:5px 0; color:#10B981; font-size:2rem; font-weight:700;">{low_risk_count}</h3>
                <span style="font-size:0.75rem; color:#10B981;">● Stable</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col5:
        st.markdown(
            f"""
            <div class="glass-card" style="padding:15px; text-align:center; height:130px; margin-bottom:10px;">
                <p style="margin:0; font-size:0.85rem; color:#64748B; font-weight:600;">Today's Runs</p>
                <h3 style="margin:5px 0; color:#7C3AED; font-size:2rem; font-weight:700;">{today_preds_count}</h3>
                <span style="font-size:0.75rem; color:#7C3AED;">● Active System</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Smart clinical Quote & Notifications row
    col_quote, col_notif = st.columns([3, 2])
    with col_quote:
        st.markdown('<div class="glass-card" style="padding: 18px; min-height: 120px;">', unsafe_allow_html=True)
        st.markdown("<h5 style='margin:0; color:#2563EB; font-weight:700;'>💡 Daily Kidney Health Note</h5>", unsafe_allow_html=True)
        # Select quote dynamically based on weekday
        quotes = [
            "Early stage chronic kidney disease has no symptoms. Regular GFR screening in diabetic and hypertensive patients is key to preserving nephrons.",
            "NSAIDs block renal prostaglandins, causing renal afferent vasoconstriction. Recommend acetaminophen for chronic pain control in CKD patients.",
            "Sustained glycemic control below HbA1c 7.0% reduces the hyperfiltration injury phase in diabetic kidney disease dramatically.",
            "Controlling systolic blood pressure to under 130 mmHg is the single most effective intervention to delay GFR decline.",
            "Water intake helps renal clearance of solutes. However, fluid restriction must be carefully applied in Stage 4/5 patients with severe edema.",
            "Hyperkalemia in advanced CKD is a cardiovascular emergency. Limit high-potassium intake (avocados, bananas, spinach) in high-risk patients.",
            "Albuminuria is an independent predictor of overall cardiovascular risk, not just renal failure. Keep ACR tracked."
        ]
        q_idx = datetime.now().weekday() % len(quotes)
        st.markdown(f"<p style='font-style: italic; color:#475569; margin-top:8px; font-size:0.95rem;'>\"{quotes[q_idx]}\"</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_notif:
        st.markdown('<div class="glass-card" style="padding: 18px; min-height: 120px;">', unsafe_allow_html=True)
        st.markdown(f"<h5 style='margin:0; color:#EF4444; font-weight:700;'>🔔 Notification Center ({active_alerts_count})</h5>", unsafe_allow_html=True)
        if active_alerts_count > 0:
            latest_alert = active_alerts[0]
            st.markdown(f"<p style='margin: 8px 0 0 0; font-size: 0.9rem; color:#EF4444;'>⚡ <b>Urgent Alert:</b> Patient <b>{latest_alert['patient_name']}</b> ({latest_alert['patient_id']}) predicted at High Risk.</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='margin: 8px 0 0 0; font-size: 0.9rem; color:#10B981;'>✅ All patient clinical metrics currently stable.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Interactive charts row
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0 0 15px 0; color:#1E3A8A; font-weight:700;'>Pie Chart: Patient Risk Distribution</h4>", unsafe_allow_html=True)
        
        # Risk distribution chart
        risk_counts = df_latest['risk_level'].value_counts().reset_index()
        risk_counts.columns = ['Risk Level', 'Count']
        
        # Color mapping matching primary, secondary, danger theme
        color_map = {
            'Low Risk': '#10B981',      # green
            'Moderate Risk': '#F59E0B', # orange/yellow
            'High Risk': '#EF4444'      # red
        }
        
        fig_pie = px.pie(
            risk_counts, 
            values='Count', 
            names='Risk Level',
            color='Risk Level',
            color_discrete_map=color_map,
            hole=0.4,
            height=280
        )
        fig_pie.update_traces(textinfo='percent+value', hoverinfo='label')
        fig_pie.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_chart2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0 0 15px 0; color:#1E3A8A; font-weight:700;'>Trend Analysis: Historical Runs</h4>", unsafe_allow_html=True)
        
        # Format prediction date to show only YYYY-MM-DD
        df['date_only'] = df['prediction_date'].str.slice(0, 10)
        trend_df = df.groupby(['date_only', 'risk_level']).size().reset_index(name='runs')
        
        fig_trend = px.bar(
            trend_df,
            x='date_only',
            y='runs',
            color='risk_level',
            color_discrete_map=color_map,
            labels={'date_only': 'Prediction Date', 'runs': 'Number of Assessments', 'risk_level': 'Risk Level'},
            height=280,
            barmode='stack'
        )
        fig_trend.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            xaxis=dict(tickangle=0)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Demographics and Clinical Features row
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0 0 15px 0; color:#1E3A8A; font-weight:700;'>Demographic: Gender & Age Risk Spread</h4>", unsafe_allow_html=True)
        
        # Age distribution colored by risk
        fig_scatter = px.scatter(
            df_latest,
            x='patient_age',
            y='kidney_health_score',
            color='risk_level',
            color_discrete_map=color_map,
            symbol='patient_gender',
            labels={'patient_age': 'Age (Years)', 'kidney_health_score': 'Kidney Health Score (0-100)', 'risk_level': 'Risk Level', 'patient_gender': 'Gender'},
            height=280
        )
        fig_scatter.update_traces(marker=dict(size=12, opacity=0.85))
        fig_scatter.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_chart4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0 0 15px 0; color:#1E3A8A; font-weight:700;'>Clinic Features: Creatinine vs Urea Log</h4>", unsafe_allow_html=True)
        
        # Creatinine vs Urea scatter
        creatinine_vals = []
        urea_vals = []
        for inp in df_latest['inputs']:
            creatinine_vals.append(inp.get('serum_creatinine', 1.0))
            urea_vals.append(inp.get('blood_urea', 40.0))
        
        df_latest['Creatinine'] = creatinine_vals
        df_latest['Urea'] = urea_vals
        
        fig_sc_ur = px.scatter(
            df_latest,
            x='Creatinine',
            y='Urea',
            color='risk_level',
            color_discrete_map=color_map,
            hover_name='patient_name',
            labels={'Creatinine': 'Serum Creatinine (mg/dL)', 'Urea': 'Blood Urea (mg/dL)'},
            height=280
        )
        fig_sc_ur.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))
        fig_sc_ur.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_sc_ur, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Alerts Feed
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin:0 0 10px 0; color:#EF4444; font-weight:700;'>🚨 Recent Critical Alerts</h4>", unsafe_allow_html=True)
    if active_alerts:
        alert_data = []
        for al in active_alerts[:5]:
            alert_data.append({
                "Alert ID": f"AL-{al['id']:04d}",
                "Patient ID": al['patient_id'],
                "Patient Name": al['patient_name'],
                "Message": al['alert_message'],
                "Logged Time": al['created_at'][:16].replace('T', ' ')
            })
        st.table(pd.DataFrame(alert_data))
    else:
        st.success("No active critical alerts. All patients have normal risk evaluations.")
    st.markdown('</div>', unsafe_allow_html=True)
