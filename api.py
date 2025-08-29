from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# __define-ocg__: FastAPI serving script for predictions

# Load the trained model
try:
    model = joblib.load("model.pkl")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Initialize FastAPI app
app = FastAPI()

# Request schema
class UserInput(BaseModel):
    prev_day_users: int

# Prediction endpoint
@app.post("/predict")
def predict(input: UserInput):
    try:
        X = np.array([[input.prev_day_users]])
        prediction = model.predict(X)[0]
        return {"predicted_daily_users": round(prediction, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")