import streamlit as st
import os
from database import init_dbs, get_chat_history, add_chat_msg, clear_chat_history, get_active_alerts, USERS_DB
from login import show_login_page
from register import show_register_page
from dashboard import show_dashboard_page
from prediction import show_prediction_page, play_high_risk_audio_alert
from patient_history import show_history_page
from reports import show_reports_page
from settings import show_settings_page
from utils import inject_custom_css, get_base64_image
from ai_summary import get_chatbot_response

# 1. Page Configuration (must be called first)
st.set_page_config(
    page_title="NephroGuard AI - Kidney Risk Alert System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Database Initialization
init_dbs()

# 3. Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "Login"
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home Dashboard"
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False
if "emergency_triggered" not in st.session_state:
    st.session_state["emergency_triggered"] = None

# 4. Styling Customization Injection
inject_custom_css(dark_mode=st.session_state["dark_mode"])

# Helper function to show Chat Assistant View
def show_chat_page():
    st.markdown('<h2 style="font-weight:700; color:#1E3A8A; margin-bottom: 2px;">💬 AI Medical Chat Assistant</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; margin-bottom: 25px;">Ask NephroGuard AI clinical questions, dietary queries, prevention guidelines, or emergency warning signs.</p>', unsafe_allow_html=True)
    
    username = st.session_state["user"]["username"]
    
    # Reset/Clear History Button in columns
    col_t1, col_t2 = st.columns([5, 1])
    with col_t2:
        if st.button("🗑️ Clear History", use_container_width=True):
            clear_chat_history(username)
            st.success("Chat history cleared.")
            st.rerun()
            
    # Load and display Chat History
    history = get_chat_history(username)
    
    st.markdown('<div class="glass-card" style="padding:15px; margin-bottom:15px;">', unsafe_allow_html=True)
    if not history:
        st.markdown(
            """
            <div style='text-align:center; padding:30px; color:#64748B;'>
                <h3>👋 Welcome to NephroGuard AI Chat</h3>
                <p>Ask questions like: "What is a healthy diet for GFR Stage 3?" or "How does creatinine affect risk?"</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        for msg in history:
            role = msg["role"]
            message = msg["message"]
            
            if role == "user":
                with st.chat_message("user"):
                    st.write(message)
            else:
                with st.chat_message("assistant", avatar="assets/logo.png"):
                    st.write(message)
    st.markdown('</div>', unsafe_allow_html=True)
                    
    # User Input
    user_query = st.chat_input("Type your query here...")
    
    if user_query:
        # Display immediately in UI
        with st.chat_message("user"):
            st.write(user_query)
            
        # Get AI Response
        response = get_chatbot_response(user_query, len(history))
        
        # Display assistant response immediately
        with st.chat_message("assistant", avatar="assets/logo.png"):
            st.write(response)
            
        # Save to database
        add_chat_msg(username, "user", user_query)
        add_chat_msg(username, "assistant", response)
        
        st.rerun()

# 5. Routing Page Flow
if not st.session_state["logged_in"]:
    # Center login/register form
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    with col_c2:
        if st.session_state["auth_page"] == "Login":
            show_login_page()
        else:
            show_register_page()
else:
    # Render Logged In Sidebar Navigation
    user = st.session_state["user"]
    logo_base64 = get_base64_image("assets/logo.png")
    
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; padding: 15px 0;">
            <img src="data:image/png;base64,{logo_base64}" width="80" style="filter: drop-shadow(0px 2px 4px rgba(37,99,235,0.25));">
            <h3 style="margin:8px 0 0 0; color:#1E3A8A; font-weight:700;">NephroGuard AI</h3>
            <p style="font-size:0.8rem; color:#64748B; margin:0;">Active Clinician Portal</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Sidebar Clinician Card
    st.sidebar.markdown(
        f"""
        <div style="background: rgba(37, 99, 235, 0.08); border: 1px solid rgba(37, 99, 235, 0.15); border-radius: 12px; padding: 12px; margin-bottom: 20px;">
            <p style="margin:0; font-size:0.8rem; color:#475569;">🏥 <b>{user['hospital']}</b></p>
            <p style="margin:4px 0 0 0; font-size:0.9rem; font-weight:700; color:#1E3A8A;">Dr. {user['fullname']}</p>
            <p style="margin:0; font-size:0.75rem; color:#64748B;">Role: {user['role']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Navigation list
    pages = {
        "Home Dashboard": "🏠 Home Dashboard",
        "Prediction Engine": "🧪 Prediction Engine",
        "Patient History": "📋 Patient History",
        "Clinical Reports": "📂 Clinical Reports",
        "AI Chat Assistant": "💬 AI Chat Assistant",
        "Settings": "⚙️ Settings"
    }
    
    selected_page_label = st.sidebar.radio(
        "Navigation Menu",
        options=list(pages.values()),
        index=list(pages.keys()).index(st.session_state["current_page"])
    )
    
    # Find matching page key
    current_page_key = [k for k, v in pages.items() if v == selected_page_label][0]
    st.session_state["current_page"] = current_page_key
    
    st.sidebar.markdown("---")
    
    # 🚨 One-Click Emergency Alert Button
    st.sidebar.markdown("<h5 style='color:#EF4444; font-weight:700; margin-bottom:8px;'>🚨 Emergency Warning Desk</h5>", unsafe_allow_html=True)
    
    # Input field inside sidebar to trigger quick emergency report
    emerg_patient_id = st.sidebar.text_input("Enter Patient ID for Alert", placeholder="e.g. P-1001", key="emerg_pid_input")
    
    st.sidebar.markdown('<div class="danger-btn">', unsafe_allow_html=True)
    trigger_emerg = st.sidebar.button("⚠️ TRIGGER EMERGENCY SIGNAL", use_container_width=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    if trigger_emerg:
        if emerg_patient_id.strip():
            # Validate patient exists
            from database import get_patient, add_prediction, add_alert
            pat = get_patient(emerg_patient_id.strip())
            if pat:
                # Log an emergency prediction representing 99% probability
                raw_inputs = {
                    "age": float(pat["age"]),
                    "gender": 1.0 if pat["gender"] == "Male" else 0.0,
                    "height": float(pat["height"]),
                    "weight": float(pat["weight"]),
                    "blood_pressure": 170.0, "blood_glucose": 210.0, "serum_creatinine": 6.5,
                    "blood_urea": 130.0, "albumin": 5.0, "hemoglobin": 8.0, "sodium": 128.0, "potassium": 6.2,
                    "hypertension": 1.0, "diabetes": 1.0, "smoking": 1.0, "alcohol": 0.0, "family_history": 1.0
                }
                pred_id = add_prediction(
                    patient_id=emerg_patient_id.strip(),
                    model_name="Manual Emergency Signal",
                    probability=0.99,
                    risk_level="High Risk",
                    score=1.0,
                    inputs_dict=raw_inputs,
                    ai_summary="CRITICAL: Manual Clinical Emergency Override Signal triggered by clinician."
                )
                alert_msg = f"CRITICAL OVERRIDE: Clinician triggered manual emergency status for Patient {pat['name']} ({emerg_patient_id}). Extreme uremia risk."
                add_alert(emerg_patient_id.strip(), pred_id, "High Risk", alert_msg)
                
                # Save emergency state
                st.session_state["emergency_triggered"] = {
                    "name": pat["name"],
                    "id": emerg_patient_id.strip()
                }
                st.success("Emergency logged! Audio/Visual sirens active.")
                st.rerun()
            else:
                st.sidebar.error("Patient ID not found in records.")
        else:
            st.sidebar.error("Please enter a Patient ID.")
            
    # Logout Button at bottom of sidebar
    st.sidebar.markdown("<br/><br/>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Clinician Sign Out", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["current_page"] = "Home Dashboard"
        st.rerun()
        
    # Render global warning alert if emergency is active
    if st.session_state["emergency_triggered"]:
        emerg_info = st.session_state["emergency_triggered"]
        st.markdown(
            f"""
            <div class="blinking-alert" style="margin-bottom:20px;">
                <h3 style="margin:0;">🚨 ACTIVE CLINICAL SIREN: EMERGENCY override ACTIVE</h3>
                <p style="margin:4px 0 0 0; font-size:1.05rem;">
                    Patient <b>{emerg_info['name']} ({emerg_info['id']})</b> has been placed on high alert. Audio warning broadcasted.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Play the alarm
        play_high_risk_audio_alert(emerg_info["name"])
        
        # Clear Alert Button
        if st.button("✅ Clear Active Siren & Reset Override"):
            st.session_state["emergency_triggered"] = None
            st.rerun()

    # Page routing display
    if st.session_state["current_page"] == "Home Dashboard":
        show_dashboard_page()
    elif st.session_state["current_page"] == "Prediction Engine":
        show_prediction_page()
    elif st.session_state["current_page"] == "Patient History":
        show_history_page()
    elif st.session_state["current_page"] == "Clinical Reports":
        show_reports_page()
    elif st.session_state["current_page"] == "AI Chat Assistant":
        show_chat_page()
    elif st.session_state["current_page"] == "Settings":
        show_settings_page()
