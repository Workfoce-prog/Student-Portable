
import streamlit as st
import pandas as pd
from datetime import datetime
import os

try:
    from googletrans import Translator
    translator = Translator()
except ImportError:
    translator = None

st.set_page_config(page_title="StratAI Auto-Translate Portal", layout="wide")

# Sidebar language selection
lang = st.sidebar.selectbox("🌍 Select Language", ["en", "fr", "es", "sw", "ar"], format_func=lambda x: {
    "en": "English", "fr": "Français", "es": "Español", "sw": "Swahili", "ar": "العربية"
}[x])

def translate(text, dest=lang):
    if dest == "en" or not translator:
        return text
    try:
        return translator.translate(text, dest=dest).text
    except:
        return text

st.title("🔐 " + translate("LOG IN TO STUDENT PORTAL"))

# Upload CSV and enable demo mode
uploaded_file = st.sidebar.file_uploader(translate("Upload custom student CSV"), type="csv")
demo_mode = st.sidebar.checkbox(translate("Enable Demo Mode (no login)"), value=False)

# Load default or uploaded data
df_students = pd.read_csv(uploaded_file) if uploaded_file else pd.read_csv("student_services_full_data.csv")
df_academic = pd.read_csv("academic_info.csv")

selected_id = str(df_students["StudentID"].iloc[0]) if demo_mode else st.text_input(translate("Enter Student ID"))

if demo_mode or (selected_id and selected_id in df_students["StudentID"].astype(str).tolist()):
    student = df_students[df_students["StudentID"].astype(str) == selected_id].iloc[0]
    academic = df_academic[df_academic["StudentID"] == int(selected_id)].iloc[0]

    st.success(f"{translate('Welcome')}, {student['Name']}!")

    st.subheader(translate("📘 Tuition Payment"))
    balance = float(student.TotalTuitionDue - student.AmountPaid)
    amount = st.number_input(translate("Payment Amount"), 0.0, float(balance), step=10.0)
    method = st.selectbox(translate("Payment Method"), ["Credit Card", "Bank Transfer", "Cash"])
    note = st.text_input(translate("Reference Note"))

    if st.button(translate("Submit Payment")):
        receipt_id = f"R-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        log = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "StudentID": student.StudentID,
            "Name": student.Name,
            "Amount": amount,
            "Method": method,
            "ReceiptID": receipt_id,
            "Note": note
        }
        log_df = pd.DataFrame([log])
        if os.path.exists("payments_log.csv"):
            old = pd.read_csv("payments_log.csv")
            log_df = pd.concat([old, log_df], ignore_index=True)
        log_df.to_csv("payments_log.csv", index=False)
        st.success(translate("Payment submitted") + f" ✅ Receipt ID: {receipt_id}")
else:
    st.warning(translate("Enter a valid Student ID to access the portal."))
