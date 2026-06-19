import streamlit as st
import pandas as pd
import plotly.express as px

from utils.s3_loader import load_analytics_bundle


st.set_page_config(
    page_title="Getaround Delay Analysis",
    page_icon="🚗",
    layout="wide"
)

bundle = load_analytics_bundle()

executive = bundle["executive_summary"]
answers = bundle["business_answers"]
distribution = bundle["delay_distribution"]
recommendation = bundle["recommendation"]

RECOMMENDED_THRESHOLD = executive["recommended_threshold"]

st.title("🚗 Getaround Rental Delay Analysis")


# EXECUTIVE SUMMARY


st.header("📋 Summary")

st.success(
    f"""
    Recommended threshold: {RECOMMENDED_THRESHOLD} minutes

    This threshold provides the best benefit-to-cost ratio.

    It solves approximately {executive['solved_cases_pct']}% of
    problematic situations while affecting only
    {executive['affected_rentals_pct']}% of successive rentals.
    """
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Threshold",
    f"{RECOMMENDED_THRESHOLD} min"
)

col2.metric(
    "Scope",
    "All Cars"
)

col3.metric(
    "Solved Cases",
    f"{executive['solved_cases_pct']}%"
)

col4.metric(
    "Affected Rentals",
    f"{executive['affected_rentals_pct']}%"
)

st.divider()


# QUESTION 1


st.header(
    "1️⃣ How many rentals would be affected by the feature?"
)

st.metric(
    "Affected Rentals",
    f"{answers['rental_impact']['affected_rentals_pct']}%"
)

st.write(
    answers["rental_impact"]["interpretation"]
)

affected_df = pd.DataFrame(
    bundle["figures"]["affected_curve"]
)

fig = px.line(
    affected_df,
    x="threshold",
    y="value",
    markers=True,
    title="Affected Rentals vs Threshold"
)

fig.add_vline(
    x=RECOMMENDED_THRESHOLD,
    line_dash="dash",
    annotation_text="Recommended"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()


# QUESTION 2


st.header(
    "2️⃣ Should the feature be enabled for all cars or only Connect vehicles?"
)

scope_df = pd.DataFrame(
    {
        "Rental Type": [
            "Connect",
            "Mobile"
        ],
        "Affected Rentals": [
            answers["scope_decision"]["affected_connect"],
            answers["scope_decision"]["affected_mobile"]
        ]
    }
)

fig = px.bar(
    scope_df,
    x="Rental Type",
    y="Affected Rentals",
    title=f"Affected Rentals at {RECOMMENDED_THRESHOLD}-Minute Threshold"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.write(
    answers["scope_decision"]["interpretation"]
)

st.divider()


# QUESTION 3


st.header("3️⃣ How often are drivers late?")

st.metric(
    "Late Checkout Rate",
    f"{answers['driver_lateness']['value_pct']}%"
)

st.write(
    answers["driver_lateness"]["interpretation"]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Median Delay",
    f"{distribution['median_minutes']} min"
)

col2.metric(
    "75th Percentile",
    f"{distribution['p75_minutes']} min"
)

col3.metric(
    "90th Percentile",
    f"{distribution['p90_minutes']} min"
)

col4.metric(
    "95th Percentile",
    f"{distribution['p95_minutes']} min"
)

st.info(
    """
    Most delays remain relatively small, but a minority of rentals
    experience very large delays.

    This long-tail behavior is what creates operational risk.
    """
)

st.divider()


# QUESTION 4


st.header(
    "4️⃣ How often does lateness impact the next driver?"
)

col1, col2 = st.columns(2)

col1.metric(
    "Impacted Rentals",
    answers["next_driver_impact"]["count"]
)

col2.metric(
    "Impact Rate",
    f"{answers['next_driver_impact']['value_pct']}%"
)

st.write(
    answers["next_driver_impact"]["interpretation"]
)

st.divider()


# QUESTION 5


st.header(
    "5️⃣ How many problematic situations would be solved?"
)

st.metric(
    "Solved Problematic Cases",
    f"{answers['problem_resolution']['solved_cases_pct']}%"
)

solved_df = pd.DataFrame(
    bundle["figures"]["solved_curve"]
)

fig = px.line(
    solved_df,
    x="threshold",
    y="value",
    markers=True,
    title="Solved Cases vs Threshold"
)

fig.add_vline(
    x=RECOMMENDED_THRESHOLD,
    line_dash="dash",
    annotation_text="Recommended"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.write(
    answers["problem_resolution"]["interpretation"]
)

st.divider()


# QUESTION 6


st.header(
    "6️⃣ At what point does increasing the threshold stop providing meaningful benefits?"
)

slope_df = pd.DataFrame(
    bundle["figures"]["benefit_slope_curve"]
)

fig = px.line(
    slope_df,
    x="threshold",
    y="value",
    markers=True,
    title="Marginal Benefit of Increasing the Threshold"
)

fig.add_vline(
    x=RECOMMENDED_THRESHOLD,
    line_dash="dash",
    annotation_text="Recommended"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    The marginal benefit decreases rapidly as the threshold increases.

    Beyond one hour, additional protection becomes increasingly
    expensive in terms of rental availability.
    """
)

st.divider()


# QUESTION 7


st.header(
    "7️⃣ Is the additional protection worth the operational cost?"
)

comparison_df = pd.DataFrame(
    {
        "Threshold": affected_df["threshold"],
        "Affected Rentals %": affected_df["value"],
        "Solved Cases %": solved_df["value"]
    }
)

fig = px.line(
    comparison_df,
    x="Threshold",
    y=[
        "Affected Rentals %",
        "Solved Cases %"
    ],
    markers=True,
    title="Customer Protection vs Business Cost"
)

fig.add_vline(
    x=RECOMMENDED_THRESHOLD,
    line_dash="dash",
    annotation_text="Recommended"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    f"""
    At {RECOMMENDED_THRESHOLD} minutes:

    • Approximately {executive['solved_cases_pct']}% of problematic situations are solved

    • Approximately {executive['affected_rentals_pct']}% of successive rentals are affected

    Increasing the threshold further provides only limited additional protection
    while significantly increasing business impact.

    Therefore {RECOMMENDED_THRESHOLD} minutes provides the best benefit-to-cost ratio.
    """
)

st.divider()


# FINAL RECOMMENDATION


st.header("➡️ Final Recommendation")

st.success(
    f"""
    Recommended Threshold: {RECOMMENDED_THRESHOLD} minutes

    Recommended Scope: All Cars

    Expected Outcomes :

    - {executive['solved_cases_pct']}% problematic situations solved

    - {executive['affected_rentals_pct']}% successive rentals affected

    - Significant reduction in customer friction

    - Best operational trade-off
    """
)