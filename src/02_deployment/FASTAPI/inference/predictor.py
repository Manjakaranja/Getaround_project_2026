import pandas as pd


FEATURE_ORDER = [
    "model_key",
    "mileage",
    "engine_power",
    "fuel",
    "paint_color",
    "car_type",
    "private_parking_available",
    "has_gps",
    "has_air_conditioning",
    "automatic_car",
    "has_getaround_connect",
    "has_speed_regulator",
    "winter_tires",
]


def predict_prices(
    model,
    payload
):

    rows = [
        item.model_dump()
        for item in payload.input
    ]

    df = pd.DataFrame(rows)

    df["mileage"] = df["mileage"].astype(float)
    df["engine_power"] = df["engine_power"].astype(float)

    df = df[FEATURE_ORDER]

    predictions = model.predict(df)

    return predictions.tolist()