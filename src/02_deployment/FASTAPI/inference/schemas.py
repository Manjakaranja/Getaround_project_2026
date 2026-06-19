from typing import List

from pydantic import BaseModel


class CarFeatures(BaseModel):

    model_key: str

    mileage: float

    engine_power: float

    fuel: str

    paint_color: str

    car_type: str

    private_parking_available: bool

    has_gps: bool

    has_air_conditioning: bool

    automatic_car: bool

    has_getaround_connect: bool

    has_speed_regulator: bool

    winter_tires: bool


class PredictionRequest(BaseModel):

    input: List[CarFeatures]


class PredictionResponse(BaseModel):

    prediction: List[float]