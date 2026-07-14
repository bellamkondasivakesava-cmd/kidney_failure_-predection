import streamlit as st
from auth import register_user
from utils import get_base64_image

def show_register_page():
    logo_base64 = get_base64_image("assets/logo.png")
    
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{logo_base64}" width="100" style="filter: drop-shadow(0px 4px 8px rgba(37,99,235,0.3));">
            <h1 class="main-title">NephroGuard AI</h1>
            <p class="sub-title">Intelligent Kidney Risk Alert System</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 📝 Register Clinician Account")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            fullname = st.text_input("Full Name", placeholder="e.g. Dr. Jane Doe")
            email = st.text_input("Email Address", placeholder="e.g. jane.doe@hospital.com")
            phone = st.text_input("Phone Number", placeholder="e.g. +1 555-0199")
            hospital = st.text_input("Hospital Name", placeholder="e.g. Mayo Clinic Nephrology")
        with col2:
            role = st.selectbox("Role / Specialty", ["Nephrologist", "Primary Care Physician", "Medical Resident", "Clinical Nurse", "System Admin"])
            username = st.text_input("Choose Username", placeholder="e.g. drjanedoe")
            password = st.text_input("Password", type="password", placeholder="At least 8 characters + symbols")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-type password")
            
        agree_terms = st.checkbox("I agree to the Terms of Service & Medical Data Security Policy")
        
        submitted = st.form_submit_button("Register Account")
        
        if submitted:
            success, msg = register_user(
                fullname=fullname.strip(),
                email=email.strip(),
                phone=phone.strip(),
                hospital=hospital.strip(),
                role=role,
                username=username.strip(),
                password=password,
                confirm_password=confirm_password,
                agree_terms=agree_terms
            )
            if success:
                st.success("Registration Successful! You can now log in.")
                st.session_state["auth_page"] = "Login"
                st.rerun()
            else:
                st.error(msg)
                
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Already have an account? Login", key="goto_login_btn"):
        st.session_state["auth_page"] = "Login"
        st.rerun()
