from tensorflow import keras
import joblib
import numpy as np
import pandas as pd

model_path = "saved_models/predictive_mantainance_mlp_model.keras"
scaler_path = "saved_models/scaler.pkl"

# Mapping from API keys to model input columns
rename_map = {
    "ProcessTemp": "Process temperature [K]",
    "ToolWear": "Tool wear [min]",
    "Power": "Power [W]",
    "TempDiff": "Temp_diff_air_process",
    "Type_H": "Type_H",
    "Type_L": "Type_L",
    "Type_M": "Type_M"
}

def load_model():
    try:
        return keras.models.load_model(model_path, compile=False)
    except Exception as e:
        raise RuntimeError(f"❌ Error loading model: {e}")

def preprocess_input(data):
    try:
        df = pd.DataFrame([data])
        df = df.rename(columns=rename_map)
        scaler = joblib.load(scaler_path)
        scaled = scaler.transform(df)
        return scaled
    except Exception as e:
        raise ValueError(f"❌ Preprocessing failed: {e}")

def predict_failure(model, data):
    try:
        processed = preprocess_input(data)
        preds = model.predict(processed)
        predicted_class = int(np.argmax(preds))
        return predicted_class
    except Exception as e:
        raise RuntimeError(f"❌ Prediction failed: {e}")