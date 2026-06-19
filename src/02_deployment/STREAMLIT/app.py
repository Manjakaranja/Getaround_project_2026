import streamlit as st

st.set_page_config(
    page_title="Getaround Analytics & Pricing",
    page_icon="🚗",
    layout="wide"
)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("images/getaround_logo.png", width=1000)

st.markdown(
    """
    <h1 style='text-align:center;'>
        Analytics & Pricing Platform
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center;font-size:18px;'>
        Analyze rental delays and estimate vehicle rental prices using
        data analytics and machine learning.
    </p>
    """,
    unsafe_allow_html=True
)
st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("Delay Analysis")

    st.markdown(
        """
        - Driver lateness analysis
        - Customer impact assessment
        - Threshold optimization
        - Business recommendations
        """
    )

    st.info("Open the Dashboard page from the sidebar")

with col2:

    st.subheader("Pricing Simulator")

    st.markdown(
        """
        - Vehicle configuration
        - Rental price prediction
        - MLflow Champion Model
        - FastAPI inference API
        """
    )

    st.info("Open the Pricing Simulator page from the sidebar")

st.divider()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Delay Analysis",
    "Completed"
)

c2.metric(
    "Champion Model",
    "Gradient Boosting"
)

c3.metric(
    "Deployment",
    "FastAPI"
)

st.success(
    "Use the sidebar to access the Dashboard and Pricing Simulator."
)