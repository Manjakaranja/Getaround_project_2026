import streamlit as st
import requests


FASTAPI_URL = (
    "https://stoneray-fastapi-getaround.hf.space/predict"
)

st.set_page_config(
    page_title="Pricing Simulator",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Getaround Pricing Simulator")

st.markdown(
    """
    Configure a vehicle and estimate its recommended daily rental price
    using the production Machine Learning model.
    """
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚗 Vehicle Information")

    model_key = st.selectbox(
        "Vehicle Brand",
        [
            "Alfa Romeo",
            "Audi",
            "BMW",
            "Citroën",
            "Ferrari",
            "Fiat",
            "Ford",
            "Honda",
            "KIA Motors",
            "Lamborghini",
            "Lexus",
            "Maserati",
            "Mazda",
            "Mercedes",
            "Mitsubishi",
            "Nissan",
            "Opel",
            "PGO",
            "Peugeot",
            "Porsche",
            "Renault",
            "SEAT",
            "Subaru",
            "Suzuki",
            "Toyota",
            "Volkswagen",
            "Yamaha"
        ],
        index=2
    )

    fuel = st.selectbox(
        "Fuel Type",
        [
            "diesel",
            "electro",
            "hybrid_petrol",
            "petrol"
        ],
        index=3
    )

    paint_color = st.selectbox(
        "Paint Color",
        [
            "beige",
            "black",
            "blue",
            "brown",
            "green",
            "grey",
            "orange",
            "red",
            "silver",
            "white"
        ],
        index=1
    )

    car_type = st.selectbox(
        "Vehicle Type",
        [
            "convertible",
            "coupe",
            "estate",
            "hatchback",
            "sedan",
            "subcompact",
            "suv",
            "van"
        ],
        index=4
    )

    mileage = st.slider(
        "Mileage (km)",
        min_value=0,
        max_value=300000,
        value=120000,
        step=5000
    )

    engine_power = st.slider(
        "Engine Power (HP)",
        min_value=20,
        max_value=800,
        value=110,
        step=5
    )

with col2:

    st.subheader("⚙️ Vehicle Options")

    private_parking_available = st.toggle(
        "Private Parking Available",
        value=True
    )

    has_gps = st.toggle(
        "GPS",
        value=True
    )

    has_air_conditioning = st.toggle(
        "Air Conditioning",
        value=True
    )

    automatic_car = st.toggle(
        "Automatic Transmission",
        value=False
    )

    has_getaround_connect = st.toggle(
        "Getaround Connect",
        value=True
    )

    has_speed_regulator = st.toggle(
        "Speed Regulator",
        value=True
    )

    winter_tires = st.toggle(
        "Winter Tires",
        value=False
    )

st.divider()

predict_button = st.button(
    "💰 Predict Daily Price",
    use_container_width=True
)

if predict_button:

    payload = {
        "input": [
            {
                "model_key": model_key,
                "mileage": float(mileage),
                "engine_power": float(engine_power),
                "fuel": fuel,
                "paint_color": paint_color,
                "car_type": car_type,
                "private_parking_available": private_parking_available,
                "has_gps": has_gps,
                "has_air_conditioning": has_air_conditioning,
                "automatic_car": automatic_car,
                "has_getaround_connect": has_getaround_connect,
                "has_speed_regulator": has_speed_regulator,
                "winter_tires": winter_tires
            }
        ]
    }

    try:

        with st.spinner(
            "Calling production pricing model..."
        ):

            response = requests.post(
                FASTAPI_URL,
                json=payload,
                timeout=30
            )

        response.raise_for_status()

        prediction = (
            response.json()["prediction"][0]
        )

        st.success(
            "Prediction completed successfully."
        )

        st.metric(
            label="Recommended Daily Rental Price",
            value=f"{prediction:.2f} €"
        )

    except Exception as e:

        st.error(
            f"Prediction failed: {str(e)}"
        )

