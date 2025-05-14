
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import os
from datetime import datetime

# Use pre-hashed passwords
user_data = {
    "usernames": {
        "admin@example.com": {
            "name": "Admin User",
            "password": "$2b$12$QLVXhIChgcRDAGB9V3ltaubC5crEuRHTj3fMp6TGknZm3/6elFdly",
            "role": "admin"
        },
        "student1@example.com": {
            "name": "Student One",
            "password": "$2b$12$kRhclox4DBbt9ogm.zYgEeFdpH83KfuPMXvcizPiSx6Tb3ihciMqu",
            "role": "student"
        }
    }
}

st.set_page_config(page_title="StratAI Secure Portal", layout="wide")

authenticator = stauth.Authenticate(
    user_data,
    "stratai_cookie", "stratai_signature_key",
    cookie_expiry_days=1
)
name, auth_status, username = authenticator.login("Login", location="main")

if auth_status:
    st.sidebar.success(f"Welcome {name}")
    role = user_data["usernames"][username]["role"]

    if role == "admin":
        st.header("🧭 Admin Dashboard with Analytics")
        df_students = pd.read_csv("student_services_full_data.csv")
        df_logs = pd.read_csv("payments_log.csv") if os.path.exists("payments_log.csv") else pd.DataFrame()

        st.metric("Total Students", len(df_students))
        st.metric("Avg GPA", round(df_students["GPA"].mean(), 2))
        st.metric("Total Paid", f"${df_students['AmountPaid'].sum():,.2f}")
        st.subheader("Student Records")
        st.dataframe(df_students, use_container_width=True)
        st.subheader("Payment Logs")
        st.dataframe(df_logs.sort_values(by="Timestamp", ascending=False), use_container_width=True)

    else:
        st.header("🎓 Student Dashboard")
        df_students = pd.read_csv("student_services_full_data.csv")
        student_record = df_students[df_students["Name"].str.contains(username.split("@")[0], case=False)]
        if not student_record.empty:
            student = student_record.iloc[0]
            st.metric("GPA", student.GPA)
            st.metric("Tuition Paid", f"${student.AmountPaid}")
        else:
            st.warning("No matching student record.")

    authenticator.logout("Logout", "sidebar")

elif auth_status is False:
    st.error("Invalid login")

elif auth_status is None:
    st.info("Please log in")

st.sidebar.markdown("## 📝 Register")
if st.sidebar.button("Register"):
    st.session_state["register"] = True

if st.session_state.get("register"):
    st.subheader("📝 Student Registration")
    reg_email = st.text_input("Email")
    reg_name = st.text_input("Full Name")
    reg_pass = st.text_input("Password", type="password")
    if st.button("Submit Registration"):
        if reg_email and reg_name and reg_pass:
            st.success(f"Registered {reg_name}. Please notify admin for approval.")
        else:
            st.warning("Please complete all fields.")

st.sidebar.markdown("## 🔁 Reset Password")
if st.sidebar.button("Reset Password"):
    st.session_state["reset"] = True

if st.session_state.get("reset"):
    st.subheader("🔁 Password Reset Request")
    reset_email = st.text_input("Email")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Update Password"):
        st.success("Request submitted. Admin will validate and reset your password.")
