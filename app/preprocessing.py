import joblib

def load_scaler(path="saved_models/scaler.pkl"):
    return joblib.load(path)

def preprocess_input(df, scaler):
    return scaler.transform(df)