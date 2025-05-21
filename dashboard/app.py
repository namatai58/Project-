import streamlit as st
import streamlit as st
import requests

st.set_page_config(page_title="Predictive Maintenance", layout="centered")
st.title("🛠️ Predictive Maintenance Failure Classifier")

st.markdown("Enter machine sensor readings below:")

# Inputs
process_temp = st.number_input("Process Temperature [K]", min_value=300.0, max_value=400.0, value=340.0)
tool_wear = st.slider("Tool Wear [min]", 0, 250, 100)
power = st.number_input("Power [W]", min_value=500.0, max_value=2000.0, value=1350.0)
temp_diff = st.number_input("Temp Difference [K]", min_value=0.0, max_value=50.0, value=15.0)

machine_type = st.radio("Machine Type", ["H", "L", "M"])
type_H = 1.0 if machine_type == "H" else 0.0
type_L = 1.0 if machine_type == "L" else 0.0
type_M = 1.0 if machine_type == "M" else 0.0

input_data = {
    "ProcessTemp": process_temp,
    "ToolWear": tool_wear,
    "Power": power,
    "TempDiff": temp_diff,
    "Type_H": type_H,
    "Type_L": type_L,
    "Type_M": type_M
}

# Prediction button
if st.button("🚀 Predict Failure"):
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"🧠 Predicted Failure Class: {result['predicted_failure']}")
        else:
            st.error("❌ Prediction failed. Check FastAPI server.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

