from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import HomePricePredictor, MODEL_PATH
import os

app = FastAPI(title="Home Price Prediction API")

predictor = HomePricePredictor()

@app.on_event("startup")
async def startup_event():
    """Load the model on startup."""
    if not predictor.load(MODEL_PATH):
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Please run: python model.py")
    print("Model loaded successfully")


class PredictionRequest(BaseModel):
    years_from_now: int


class PredictionResponse(BaseModel):
    years_from_now: int
    predicted_price: float


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Predict home price for a given number of years from now."""
    try:
        price = predictor.predict(request.years_from_now)
        return PredictionResponse(
            years_from_now=request.years_from_now,
            predicted_price=price
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
