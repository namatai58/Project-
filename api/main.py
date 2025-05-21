
from fastapi import FastAPI
from pydantic import BaseModel
from app.model import load_model, predict_failure

app = FastAPI()

# Load model once at startup
model = load_model()

# Define the input schema using Pydantic
class SensorData(BaseModel):
    ProcessTemp: float
    ToolWear: float
    Power: float
    TempDiff: float
    Type_H: float
    Type_L: float
    Type_M: float

@app.post("/predict")
def predict(data: SensorData):
    input_dict = data.dict()
    prediction = predict_failure(model, input_dict)
    return {"predicted_failure": prediction}