import mlflow
import os

from config import (
    MLFLOW_TRACKING_URI,
    MODEL_URI
)


def load_champion_model():

    mlflow.set_tracking_uri(
        MLFLOW_TRACKING_URI
    )

    model = mlflow.pyfunc.load_model(
        MODEL_URI
    )

    return model