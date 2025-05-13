
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="StratAI Student Portal", layout="wide")

st.title("🎓 StratAI Student Services Portal (Beta)")

@st.cache_data
def load_data():
    df_students = pd.read_csv("student_services_full_data.csv")
    df_academic = pd.read_csv("academic_info.csv")
    return df_students, df_academic

df_students, df_academic = load_data()

student_names = df_students["Name"].tolist()
selected_student = st.selectbox("Select Student", student_names)
student = df_students[df_students["Name"] == selected_student].iloc[0]
academic = df_academic[df_academic["StudentID"] == student.StudentID].iloc[0]

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Dashboard", "📚 Academic Info", "💰 Financial Center", 
    "👨‍👩‍👧 Family View", "👤 Profile", "📘 Payment History"
])

with tab1:
    st.subheader(f"Welcome, {selected_student}")
    col1, col2, col3 = st.columns(3)
    col1.metric("GPA", student.GPA)
    col2.metric("Wellness Score", student.WellnessScore)
    col3.metric("Outstanding Tuition", f"${student.TotalTuitionDue - student.AmountPaid:,.2f}")
    st.info("Use the tabs above to explore your student services.")

with tab2:
    st.subheader("📚 Academic Info")
    st.write(f"**Academic Standing:** {academic.AcademicStanding}")
    st.write(f"**Current Credits:** {academic.CurrentCredits}")
    st.write("**Course Schedule:**")
    st.code(academic.CourseSchedule)

with tab3:
    st.subheader("💳 Make a Tuition Payment")
    st.write(f"**Current Balance:** ${student.TotalTuitionDue - student.AmountPaid:,.2f}")
    amount = st.number_input("Enter Payment Amount", min_value= 0.0, max_value=float(student.TotalTuitionDue - student.AmountPaid),step= 10.0)
    method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "Bank Transfer", "Cash", "Check"])
    note = st.text_input("Notes or Reference")
    if st.button("Submit Payment"):
        receipt_id = f"R-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        log = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "StudentID": student.StudentID,
            "Name": selected_student,
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
    st.subheader("👨‍👩‍👧 Family Portal View")
    st.write(f"**Parent Email:** {student.ParentEmail}")
    st.write(f"**Current GPA:** {student.GPA}")
    st.write(f"**Total Paid:** ${student.AmountPaid:,.2f}")
    st.write(f"**RAG Status:** {student.RAGStatus}")

with tab5:
    st.subheader("👤 Profile Overview")
    st.write("This section can include name, address, email, password reset and preferences (future version).")
    st.json({
        "Name": student.Name,
        "Student ID": int(student.StudentID),
        "Email": f"{student.Name.lower().split()[0]}@university.edu",
        "Program": "Bachelor of Arts",
        "Standing": academic.AcademicStanding
    })

with tab6:
    st.subheader("📘 Payment History")
    if os.path.exists("payments_log.csv"):
        payments = pd.read_csv("payments_log.csv")
        payments = payments[payments["StudentID"] == student.StudentID]
        if not payments.empty:
            st.dataframe(payments.sort_values(by="Timestamp", ascending=False), use_container_width=True)
        else:
            st.info("No payments yet.")
    else:
        st.info("No payment log found.")
