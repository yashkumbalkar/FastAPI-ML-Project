import streamlit as st
import requests
import threading
import time
import subprocess
import sys
import os

# Function to run FastAPI server
def run_fastapi():
    try:
        subprocess.Popen([sys.executable, "run_api.py"])
    except Exception as e:
        st.error(f"Error starting FastAPI server: {e}")

# Start FastAPI server in background
if 'fastapi_started' not in st.session_state:
    st.session_state.fastapi_started = True
    thread = threading.Thread(target=run_fastapi, daemon=True)
    thread.start()
    time.sleep(5)  # Wait for server to start

API_URL = "http://localhost:8000/predict" 

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Insurance Premium Category: **{result['Predicted_Category']}**")
        else:
            st.error(f"API Error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")
