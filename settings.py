import os
import streamlit as st
from auth import validate_password_strength, hash_password
from database import update_user_password, USERS_DB, PATIENTS_DB

def show_settings_page():
    st.markdown('<h2 style="font-weight:700; color:#1E3A8A; margin-bottom: 2px;">⚙️ Settings & Configuration</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B; margin-bottom: 25px;">Manage clinical profiles, system configurations, theme adjustments, and database backups.</p>', unsafe_allow_html=True)
    
    user = st.session_state.get("user")
    if not user:
        st.error("No active user session detected.")
        return
        
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 👤 Active Clinician Profile")
    st.markdown(
        f"""
        <table style="width:100%; border-collapse:collapse; margin-top:10px; font-size:0.95rem;">
            <tr><td style="padding:6px; font-weight:600; width:180px;">Full Name:</td><td>{user['fullname']}</td></tr>
            <tr><td style="padding:6px; font-weight:600;">Username:</td><td>{user['username']}</td></tr>
            <tr><td style="padding:6px; font-weight:600;">Email:</td><td>{user['email']}</td></tr>
            <tr><td style="padding:6px; font-weight:600;">Phone Number:</td><td>{user['phone']}</td></tr>
            <tr><td style="padding:6px; font-weight:600;">Hospital Affiliation:</td><td>{user['hospital']}</td></tr>
            <tr><td style="padding:6px; font-weight:600;">Role / Specialty:</td><td>{user['role']}</td></tr>
        </table>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Tabs for Security and Admin Tasks
    tab_sec, tab_admin = st.tabs(["🔒 Account Security & Preferences", "💾 Database & Backup Operations"])
    
    with tab_sec:
        # Theme Toggle
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("### 🌗 Theme Preferences")
        theme_dark = st.toggle("Enable Clinical Dark Mode Theme", value=st.session_state.get("dark_mode", False))
        
        if theme_dark != st.session_state.get("dark_mode", False):
            st.session_state["dark_mode"] = theme_dark
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Password update
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("### 🔑 Change Account Password")
        
        with st.form("change_password_form"):
            current_pwd = st.text_input("Current Password", type="password", placeholder="Enter current password")
            new_pwd = st.text_input("New Password", type="password", placeholder="Min 8 characters + symbols")
            confirm_new_pwd = st.text_input("Confirm New Password", type="password", placeholder="Re-type new password")
            
            submitted = st.form_submit_button("Update Password")
            
            if submitted:
                # We authenticate user with current password first
                from auth import verify_password
                if not verify_password(current_pwd, user["password"]):
                    st.error("Incorrect current password.")
                elif new_pwd != confirm_new_pwd:
                    st.error("New passwords do not match.")
                else:
                    is_strong, msg = validate_password_strength(new_pwd)
                    if is_strong:
                        new_hash = hash_password(new_pwd)
                        if update_user_password(user["username"], new_hash):
                            # Update session state user dict password field
                            st.session_state["user"]["password"] = new_hash
                            st.success("Password updated successfully!")
                        else:
                            st.error("Failed to update password.")
                    else:
                        st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_admin:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("### 📥 Export System Databases")
        st.write("Download local database files as backups for external ingestion or data compliance audits.")
        
        col_db1, col_db2 = st.columns(2)
        
        with col_db1:
            if os.path.exists(USERS_DB):
                with open(USERS_DB, "rb") as f:
                    db_bytes = f.read()
                st.download_button(
                    label="📥 Download Users Database (users.db)",
                    data=db_bytes,
                    file_name="users.db",
                    mime="application/x-sqlite3",
                    use_container_width=True
                )
            else:
                st.error("Users database file not found.")
                
        with col_db2:
            if os.path.exists(PATIENTS_DB):
                with open(PATIENTS_DB, "rb") as f:
                    db_bytes = f.read()
                st.download_button(
                    label="📥 Download Patients Database (patients.db)",
                    data=db_bytes,
                    file_name="patients.db",
                    mime="application/x-sqlite3",
                    use_container_width=True
                )
            else:
                st.error("Patients database file not found.")
                
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card" style="border-left: 5px solid #F59E0B; background: rgba(245, 158, 11, 0.03);">', unsafe_allow_html=True)
        st.write("⚠️ **Warning on Compliance:** Ensure exported databases are kept secure in accordance with clinical patient privacy rules (HIPAA/GDPR regulations). Contains sensitive credentials and diagnostics metrics.")
        st.markdown('</div>', unsafe_allow_html=True)
