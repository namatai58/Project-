# --- main.py (Improved FastAPI app) ---
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
API_KEY = os.getenv("API_KEY", "1234")  # default fallback

# Set up logging to a file
logging.basicConfig(
    filename="api_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()
model = load_model()

# Allow all CORS (can be restricted for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define expected input structure
class SensorData(BaseModel):
    ProcessTemp: float
    ToolWear: int
    Power: float
    TempDiff: float
    Type_H: float
    Type_L: float
    Type_M: float

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "🚀 Predictive Maintenance API is live!"}

# Prediction endpoint
@app.post("/predict")
def predict(data: SensorData, request: Request):
    input_dict = data.dict()

    # Simple API key check
    if request.headers.get("x-api-key") != API_KEY:
        return {"error": "❌ Invalid API Key"}

    try:
        # Failure label mapping
        failure_mapping = {
            0: 'No Failure',
            1: 'Tool Wear / Random Failures',
            2: 'Power Failure',
            3: 'Overstrain Failure',
            4: 'Heat Dissipation Failure'
        }

        # Run prediction and decode
        prediction = int(predict_failure(model, input_dict))
        failure_name = failure_mapping.get(prediction, "Unknown Failure")

        # Log entry
        log_entry = {
            "client": request.client.host,
            "input": input_dict,
            "prediction": prediction,
            "failure_name": failure_name
        }
        logging.info(json.dumps(log_entry, indent=2))

        return {
            "predicted_failure": prediction,
            "pretty_result": f"🔥 Failure Type: {failure_name}"
        }

    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        return {"error": f"❌ Prediction failed: {str(e)}"}