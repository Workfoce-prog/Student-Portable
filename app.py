
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="StratAI Student Portal", layout="wide")

st.title("🔐 LOG IN TO STUDENT PORTAL")

# Load datasets
@st.cache_data
def load_data():
    students = pd.read_csv("student_services_full_data.csv")
    academics = pd.read_csv("academic_info.csv")
    return students, academics

df_students, df_academic = load_data()

# Login simulation
student_ids = df_students["StudentID"].astype(str).tolist()
entered_id = st.text_input("Enter Student ID")
login_success = False

if entered_id and entered_id in student_ids:
    student = df_students[df_students["StudentID"].astype(str) == entered_id].iloc[0]
    academic = df_academic[df_academic["StudentID"] == int(entered_id)].iloc[0]
    login_success = True
    st.success(f"Welcome, {student['Name']}!")

if login_success:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏠 Dashboard", "📚 Academic Info", "💰 Financial Center",
        "👨‍👩‍👧 Family View", "👤 Profile", "📘 Payment History", "🔍 Browse Students"
    ])

    with tab1:
        st.subheader("Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("GPA", student.GPA)
        col2.metric("Wellness", student.WellnessScore)
        col3.metric("Outstanding Tuition", f"${student.TotalTuitionDue - student.AmountPaid:,.2f}")

    with tab2:
        st.subheader("Academic Info")
        st.write(f"Academic Standing: {academic.AcademicStanding}")
        st.write(f"Current Credits: {academic.CurrentCredits}")
        st.code(academic.CourseSchedule)

    with tab3:
        st.subheader("Tuition Payment")
        balance = float(student.TotalTuitionDue - student.AmountPaid)
        amount = st.number_input("Enter Payment Amount", 0.0, float(balance), step=10.0)
        method = st.selectbox("Payment Method", ["Credit Card", "Bank Transfer", "Cash"])
        note = st.text_input("Reference Note")
        if st.button("Submit Payment"):
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
            st.success(f"Payment submitted. Receipt ID: {receipt_id}")

    with tab4:
        st.subheader("Family Portal")
        st.write(f"Parent Email: {student.ParentEmail}")
        st.write(f"GPA: {student.GPA}, Paid: ${student.AmountPaid}, RAG: {student.RAGStatus}")

    with tab5:
        st.subheader("Profile Info")
        st.json({
            "Name": student.Name,
            "Student ID": int(student.StudentID),
            "Email": f"{student.Name.lower().split()[0]}@university.edu",
            "Program": "Bachelor of Arts",
            "Standing": academic.AcademicStanding
        })

    with tab6:
        st.subheader("Payment History")
        if os.path.exists("payments_log.csv"):
            logs = pd.read_csv("payments_log.csv")
            logs = logs[logs["StudentID"] == student.StudentID]
            if not logs.empty:
                st.dataframe(logs.sort_values(by="Timestamp", ascending=False), use_container_width=True)
            else:
                st.info("No payments recorded.")
        else:
            st.info("No payment log available.")

    with tab7:
        st.subheader("Browse All Students (Admin View)")
        st.dataframe(df_students, use_container_width=True)

else:
    st.warning("Please enter a valid Student ID to log in.")
