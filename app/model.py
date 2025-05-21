from tensorflow import keras
import joblib
import numpy as np
import pandas as pd  

model_path = "saved_models/predictive_mantainance_mlp_model.keras"
scaler_path = "saved_models/scaler.pkl"

def load_model():
    return keras.models.load_model(model_path, compile=False)

def preprocess_input(data):
    # Convert API-friendly keys to training column names
    rename_map = {
        "ProcessTemp": "Process temperature [K]",
        "ToolWear": "Tool wear [min]",
        "Power": "Power [W]",
        "TempDiff": "Temp_diff_air_process",
        "Type_H": "Type_H",
        "Type_L": "Type_L",
        "Type_M": "Type_M"
    }

    # Convert to DataFrame and rename
    df = pd.DataFrame([data])
    df = df.rename(columns=rename_map)

    # Load scaler and transform
    scaler = joblib.load(scaler_path)
    scaled = scaler.transform(df)
    return scaled

def predict_failure(model, data):
    processed = preprocess_input(data)
    preds = model.predict(processed)
    return int(np.argmax(preds))