from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os

# Add parent directory to path to import inference
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inference import CivicMLPredictor

app = FastAPI(title="CivicML API")

# Load model using the absolute path relative to the api directory
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model", "model.pkl")
predictor = CivicMLPredictor(model_path=model_path)

class PredictRequest(BaseModel):
    text_embedding: list

@app.post("/api/predict")
def predict(req: PredictRequest):
    try:
        result = predictor.predict(req.text_embedding)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/health")
def health():
    return {"status": "ok"}

# For local development, serve the public directory
public_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
if os.path.exists(public_dir):
    app.mount("/", StaticFiles(directory=public_dir, html=True), name="public")
