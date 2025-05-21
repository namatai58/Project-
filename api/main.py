# --- main.py (FastAPI app with pretty printing, file logging, and env protection) ---
import os
import json
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from app.model import load_model, predict_failure

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY", "1234")  # default fallback for testing

# Set up logging to a file
logging.basicConfig(
    filename="api_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()
model = load_model()

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SensorData(BaseModel):
    ProcessTemp: float
    ToolWear: int
    Power: float
    TempDiff: float
    Type_H: float
    Type_L: float
    Type_M: float

@app.get("/")
def read_root():
    return {"message": "🚀 Predictive Maintenance API is live!"}

@app.post("/predict")
def predict(data: SensorData, request: Request):
    input_dict = data.dict()

    # --- Security Check (simple API key from header) ---
    if request.headers.get("x-api-key") != API_KEY:
        return {"error": "❌ Invalid API Key"}

    # --- Prediction and Logging ---
    prediction = predict_failure(model, input_dict)
    log_entry = {
        "client": request.client.host,
        "input": input_dict,
        "prediction": prediction
    }
    logging.info(json.dumps(log_entry, indent=2))

    return {"predicted_failure": prediction, "pretty_result": f"🔥 Failure Type: {prediction}"}