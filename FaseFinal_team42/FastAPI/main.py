from pydantic import BaseModel
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
import os
from pathlib import Path

app = FastAPI(
    title="Team42 ML Model API",
    description="API para realizar predicciones usando el modelo final de Gradient Boosting",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent  # /app
MODEL_PATH = BASE_DIR / "models" / "final_model_GradBoost.joblib"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model artifact not found at: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

#Mismo orden que en el modelo
class ModelInput(BaseModel):
    ContrCarPol: float
    NumCarPol: float
    ContrFirePol: float
    DemAvgIncome: float
    DemMidInc: float
    DemLoLeEdu: float
    DemHiLeEdu: float
    DemLowestInc: float
    ContrPrivIns: float
    CMainType: float
    CAR_CROSS: float
    FIRE_CROSS: float  

@app.get("/")
def root():
    return {"message": "API funcionando. Ir a /docs para probar /predict"}

@app.post("/predict")
def predict(input_data: ModelInput):
    try:
        # Convertir entrada a DataFrame
        df = pd.DataFrame([input_data.dict()])

        # Probabilidad de la clase positiva 
        proba = model.predict_proba(df)[0][1]

        # Predicción "general" del modelo 
        prediction_default = int(proba >= 0.5)

        # Predicción ajustada 
        threshold = 0.01
        prediction_adjusted = int(proba >= threshold)

        return {
            "prediction_default": prediction_default,
            "prediction_adjusted": prediction_adjusted,
            "probability": float(proba),
            "threshold_used": threshold
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))