import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env (for local development)
load_dotenv()

# Page settings
st.set_page_config(page_title="Predictive Maintenance", layout="centered")
st.title("🛠️ Predictive Maintenance Failure Classifier")
st.markdown("Enter machine sensor readings below:")

# Input fields
process_temp = st.number_input("Process Temperature [K]", min_value=300.0, max_value=400.0, value=340.0)
tool_wear = st.slider("Tool Wear [min]", 0, 250, 100)
power = st.number_input("Power [W]", min_value=500.0, max_value=2000.0, value=1350.0)
temp_diff = st.number_input("Temp Difference [K]", min_value=0.0, max_value=50.0, value=15.0)

# Machine type encoding
machine_type = st.radio("Machine Type", ["High", "Low", "Medium"])
type_H = 1.0 if machine_type == "High" else 0.0
type_L = 1.0 if machine_type == "Low" else 0.0
type_M = 1.0 if machine_type == "Medium" else 0.0

# Assemble input
input_data = {
    "ProcessTemp": process_temp,
    "ToolWear": tool_wear,
    "Power": power,
    "TempDiff": temp_diff,
    "Type_H": type_H,
    "Type_L": type_L,
    "Type_M": type_M
}

# --- Secure API settings ---
API_URL = os.getenv("API_URL", "https://project-predictive-maintenance-api.onrender.com/predict")
API_KEY = os.getenv("API_KEY", "Zimbabwe1980!@")
headers = {"x-api-key": API_KEY}

# Failure class mapping
failure_mapping = {
    0: 'No Failure',
    1: 'Tool Wear / Random Failures',
    2: 'Power Failure',
    3: 'Overstrain Failure',
    4: 'Heat Dissipation Failure',
}

# --- Prediction ---
if st.button("🚀 Predict Failure"):
    try:
        response = requests.post(API_URL, json=input_data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            failure_class = int(result.get('predicted_failure', -1))
            failure_name = failure_mapping.get(failure_class, "Unknown Failure")
            st.success(f"🧠 Predicted Failure: {failure_name}")
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"❌ Request Failed: {str(e)}")