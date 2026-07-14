import streamlit as st
import base64
from auth import authenticate_user
from database import get_user_by_username, update_user_password
from auth import validate_password_strength, hash_password
from utils import get_base64_image

def show_login_page():
    # Header Logo
    logo_base64 = get_base64_image("assets/logo.png")
    
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <img src="data:image/png;base64,{logo_base64}" width="110" style="filter: drop-shadow(0px 4px 8px rgba(37,99,235,0.3));">
            <h1 class="main-title">NephroGuard AI</h1>
            <p class="sub-title">Intelligent Kidney Risk Alert System</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Check if we are in "forgot password" mode
    if st.session_state.get("forgot_password_mode", False):
        show_forgot_password_view()
        return

    # Login Glassmorphism Card Container
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 🔐 Clinician Login")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        remember_me = st.checkbox("Remember Me")
        
        submitted = st.form_submit_button("Sign In")
        
        if submitted:
            success, msg, user = authenticate_user(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.session_state["current_page"] = "Home Dashboard"
                st.success("Login Successful! Redirecting...")
                st.rerun()
            else:
                st.error(msg)
                
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation Help Links
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Forgot Password?", key="forgot_btn"):
            st.session_state["forgot_password_mode"] = True
            st.rerun()
            
    with col2:
        if st.button("Create Account (Register)", key="goto_reg_btn"):
            st.session_state["auth_page"] = "Register"
            st.rerun()

def show_forgot_password_view():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 🔄 Forgot Password / Reset Credentials")
    st.write("For security validation, please verify your username, email and set a new password.")
    
    with st.form("reset_form"):
        username = st.text_input("Username", placeholder="Your username")
        email = st.text_input("Email Address", placeholder="Your registered email")
        new_password = st.text_input("New Password", type="password", placeholder="At least 8 characters")
        confirm_new_password = st.text_input("Confirm New Password", type="password", placeholder="Re-type new password")
        
        submitted = st.form_submit_button("Reset Password")
        
        if submitted:
            if new_password != confirm_new_password:
                st.error("Passwords do not match.")
            else:
                user = get_user_by_username(username)
                if user and user["email"].lower() == email.lower().strip():
                    is_strong, msg = validate_password_strength(new_password)
                    if is_strong:
                        new_hash = hash_password(new_password)
                        if update_user_password(username, new_hash):
                            st.success("Password reset successfully. You can now login.")
                            st.session_state["forgot_password_mode"] = False
                            st.rerun()
                        else:
                            st.error("Failed to update password. Try again.")
                    else:
                        st.error(msg)
                else:
                    st.error("Invalid username or email combination.")
                    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Back to Login", key="back_login_btn"):
        st.session_state["forgot_password_mode"] = False
        st.rerun()
