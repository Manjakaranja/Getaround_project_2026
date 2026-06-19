from fastapi import FastAPI

from inference.schemas import (PredictionRequest, PredictionResponse)

from inference.predictor import (predict_prices)

from inference.model_loader import (load_champion_model)


app = FastAPI(
    title="Getaround Pricing API",
    description="""
    Predict optimal rental prices for Getaround vehicles.

    Champion model:
    Tune_GradientBoosting

    Registry:
    getaround-pricing-model

    Alias:
    champion
    """,
    version="1.0.0"
)


model = load_champion_model()


@app.get("/")
def root():

    return {
        "message": "Getaround Pricing API"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(
    request: PredictionRequest
):

    predictions = predict_prices(
        model,
        request
    )

    return {
        "prediction": predictions
    }