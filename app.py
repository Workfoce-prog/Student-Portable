
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Universal Student Portal", layout="wide")
st.title("🎓 Universal Student Services Portal")

# Data upload
st.sidebar.header("📁 Upload Your School's Student Data")
uploaded_file = st.sidebar.file_uploader("Upload your student CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data uploaded successfully.")
else:
    st.info("Please upload a student CSV file to begin.")
    st.stop()

# Simulated dashboard
student_list = df["Name"].tolist()
selected_student = st.selectbox("Select Student", student_list)
student = df[df["Name"] == selected_student].iloc[0]

tab1, tab2 = st.tabs(["🏠 Dashboard", "💳 Tuition Payment"])

with tab1:
    st.subheader(f"Welcome, {selected_student}")
    col1, col2, col3 = st.columns(3)
    col1.metric("GPA", student["GPA"])
    col2.metric("Credits", student.get("Credits", 0))
    col3.metric("Outstanding Tuition", f"${student['TotalTuitionDue'] - student['AmountPaid']:,.2f}")

with tab2:
    st.subheader("💳 Make a Tuition Payment")
    balance = float(student["TotalTuitionDue"] - student["AmountPaid"])
    amount = st.number_input("Payment Amount", 0.0, float(balance), step=10.0)
    method = st.selectbox("Payment Method", ["Credit Card", "Bank Transfer", "Cash"])
    if st.button("Submit Payment"):
        st.success(f"Submitted payment of ${amount:,.2f} for {selected_student}")
