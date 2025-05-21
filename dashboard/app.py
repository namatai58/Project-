import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from datetime import datetime

#Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY", "Zimbabwe1980!@")
API_URL = os.getenv("API_URL", "https://project-predictive-maintenance-api.onrender.com/predict")

# File to log predictions
LOG_FILE = "prediction_log.csv"

# Failure classes
failure_mapping = {
    0: 'No Failure',
    1: 'Tool Wear / Random Failures',
    2: 'Power Failure',
    3: 'Overstrain Failure',
    4: 'Heat Dissipation Failure',
}

# --- Streamlit UI ---
st.set_page_config(page_title="Predictive Maintenance", layout="wide")
st.title("🛠️ Predictive Maintenance Failure Classifier")

# Sidebar inputs
st.sidebar.header("Machine Sensor Input")
process_temp = st.sidebar.number_input("Process Temperature [K]", min_value=300.0, max_value=400.0, value=340.0)
tool_wear = st.sidebar.slider("Tool Wear [min]", 0, 250, 100)
power = st.sidebar.number_input("Power [W]", min_value=500.0, max_value=2000.0, value=1350.0)
temp_diff = st.sidebar.number_input("Temp Difference [K]", min_value=0.0, max_value=50.0, value=15.0)

machine_type = st.sidebar.radio("Machine Type", ["High", "Low", "Medium"])
type_H = 1.0 if machine_type == "High" else 0.0
type_L = 1.0 if machine_type == "Low" else 0.0
type_M = 1.0 if machine_type == "Medium" else 0.0

input_data = {
    "ProcessTemp": process_temp,
    "ToolWear": tool_wear,
    "Power": power,
    "TempDiff": temp_diff,
    "Type_H": type_H,
    "Type_L": type_L,
    "Type_M": type_M
}

# Show JSON input
st.subheader("📦 Input JSON")
st.json(input_data)

# --- Prediction Section ---
headers = {"x-api-key": API_KEY}
if st.button("🚀 Predict Failure"):
    try:
        response = requests.post(API_URL, json=input_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            failure_class = int(result['predicted_failure'])
            failure_name = failure_mapping.get(failure_class, "Unknown Failure")
            st.success(f"🧠 Predicted Failure: {failure_name}")

            # Log prediction
            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "failure_class": failure_class,
                "failure_name": failure_name,
                **input_data
            }
            log_df = pd.DataFrame([log_entry])
            if os.path.exists(LOG_FILE):
                log_df.to_csv(LOG_FILE, mode='a', header=False, index=False)
            else:
                log_df.to_csv(LOG_FILE, index=False)
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"❌ Request Failed: {str(e)}")

# --- Analytics Section ---
st.subheader("📊 Prediction Analytics")
if os.path.exists(LOG_FILE):
    logs = pd.read_csv(LOG_FILE)
    st.metric("Total Predictions Made", len(logs))
    common = logs['failure_name'].value_counts().idxmax()
    st.metric("Most Common Failure", common)

    # Visualize class counts
    fig = px.bar(logs['failure_name'].value_counts().reset_index(),
                 x='index', y='failure_name',
                 labels={'index': 'Failure Type', 'failure_name': 'Count'},
                 title="Failure Type Distribution")
    st.plotly_chart(fig)

    # Show raw log
    st.subheader("📜 Raw Prediction Log")
    st.dataframe(logs)
else:
    st.info("No predictions logged yet.")