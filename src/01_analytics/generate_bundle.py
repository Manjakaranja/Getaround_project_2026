from pathlib import Path
import json
import pandas as pd


# PATHS


ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    ROOT_DIR
    / "data"
    / "raw"
    / "get_around_delay_analysis.xlsx"
)

OUTPUT_PATH = (
    ROOT_DIR
    / "data"
    / "outputs"
    / "analytics_bundle.json"
)


# LOAD DATA


df = pd.read_excel(DATA_PATH)

df["time_delta"] = df["time_delta_with_previous_rental_in_minutes"]
df["prev_id"] = df["previous_ended_rental_id"]
df["delay_checkout"] = df["delay_at_checkout_in_minutes"]

df = df.drop(
    columns=[
        "time_delta_with_previous_rental_in_minutes",
        "previous_ended_rental_id",
        "delay_at_checkout_in_minutes",
    ]
)

# Remove impossible checkout delays (> 1 day)
df = df[
    df["delay_checkout"].between(-1440, 1440)
    | df["delay_checkout"].isna()
].copy()


# ANALYTICAL DATASETS


df_chain = df.loc[df["time_delta"].notna()].copy()

df_delay = df.loc[df["delay_checkout"].notna()].copy()


# EXECUTIVE KPIs


late_rate = round(
    (df_delay["delay_checkout"] > 0).mean() * 100,
    2
)

df_chain["impacts_next_driver"] = (
    df_chain["delay_checkout"]
    > df_chain["time_delta"]
)

impacted_count = int(
    df_chain["impacts_next_driver"].sum()
)

impacted_pct = round(
    df_chain["impacts_next_driver"].mean() * 100,
    2
)

# MOD : total number of truly problematic situations
problematic_cases = int(
    (
        df_chain["delay_checkout"]
        > df_chain["time_delta"]
    ).sum()
)


# THRESHOLD ANALYSIS


threshold_results = []

for threshold in range(0, 721, 30):

    affected = (
        df_chain["time_delta"] < threshold
    ).sum()

    affected_pct = round(
        affected / len(df_chain) * 100,
        2
    )

    # MOD : revert to notebook logic

    solved_mask = (
        (df_chain["time_delta"] + threshold)
        > df_chain["delay_checkout"]
    )

    solved_count = int(
        solved_mask.sum()
    )

    solved_pct = round(
        solved_count / len(df_chain) * 100,
        2
    )

    efficiency = (
        round(solved_count / affected, 2)
        if affected > 0
        else None
    )

    # MOD : notebook KPI
    efficiency_pct = round(
        solved_count / affected * 100,
        2
    ) if affected > 0 else None

    threshold_results.append(
        {
            "threshold": threshold,
            "affected_rentals": int(affected),
            "affected_rentals_pct": affected_pct,
            "solved_cases": solved_count,
            "solved_cases_pct": solved_pct,
            "efficiency_pct": efficiency_pct,
        }
    )




# CONNECT VS MOBILE


connect_df = df_chain[
    df_chain["checkin_type"] == "connect"
]

mobile_df = df_chain[
    df_chain["checkin_type"] == "mobile"
]

connect_affected_60 = int(
    (connect_df["time_delta"] < 60).sum()
)

mobile_affected_60 = int(
    (mobile_df["time_delta"] < 60).sum()
)



# RECOMMENDED THRESHOLD

# MOD : recommendation comes from business analysis,
# not from an automatic optimization rule.

comparison_df = pd.DataFrame(threshold_results)

comparison_df["benefit_slope"] = (
    comparison_df["solved_cases_pct"]
    .diff()
    /
    comparison_df["threshold"]
    .diff()
)

# MOD
recommended_threshold = 60

# MOD
recommended_row = comparison_df.loc[
    comparison_df["threshold"] == recommended_threshold
].iloc[0]


# INTERPRETATION


# MOD
interpretation = (
    "A threshold of 60 minutes (1 hour) is recommended because "
    "it solves approximately 75% of problematic situations while "
    "affecting only about 21% of successive rentals. "
    "Increasing the threshold beyond 60 minutes provides only "
    "limited additional customer protection while significantly "
    "increasing the number of affected rentals. "
    "This threshold therefore provides the best benefit-to-cost ratio."
)


# CHART DATA

# MOD : ready-to-use data for Streamlit visualizations

affected_curve = [
    {
        "threshold": row["threshold"],
        "value": row["affected_rentals_pct"],
    }
    for row in threshold_results
]

solved_curve = [
    {
        "threshold": row["threshold"],
        "value": row["solved_cases_pct"],
    }
    for row in threshold_results
]

efficiency_curve = [
    {
        "threshold": row["threshold"],
        "value": row["efficiency_pct"],
    }
    for row in threshold_results
]


benefit_slope_curve = [
    {
        "threshold": int(row["threshold"]),
        "value": (
            round(
                float(row["benefit_slope"]),
                4
            )
            if pd.notna(row["benefit_slope"])
            else None
        )
    }
    for _, row in comparison_df.iterrows()
]

# BUSINESS ANSWERS


business_answers = {

    "driver_lateness": {
        "question": "How often are drivers late?",
        "value_pct": late_rate,
        "interpretation": (
            f"{late_rate}% of completed rentals ended with a late checkout. "
            "This confirms that lateness is a frequent operational event "
            "and should not be considered exceptional."
        ),
    },

    "next_driver_impact": {
        "question": (
            "How often does lateness impact the next driver?"
        ),
        "count": impacted_count,
        "value_pct": impacted_pct,
        "interpretation": (
            f"Only {impacted_pct}% of successive rentals create a direct "
            "impact on the following customer. Although late returns are "
            "common, most are absorbed by the natural gap between rentals."
        ),
    },

    "rental_impact": {
        "question": (
            "How many rentals would be affected by the "
            "recommended threshold?"
        ),
        "threshold": recommended_threshold,
        "affected_rentals": int(
            recommended_row["affected_rentals"]
        ),
        "affected_rentals_pct": float(
            recommended_row["affected_rentals_pct"]
        ),
        "interpretation": (
            f"A {recommended_threshold}-minute buffer would affect "
            f"{recommended_row['affected_rentals_pct']}% of successive "
            "rentals by making some booking combinations unavailable."
        ),
    },

    "problem_resolution": {
        "question": (
            "How many problematic situations would be solved?"
        ),
        "threshold": recommended_threshold,
        "solved_cases": int(
            recommended_row["solved_cases"]
        ),
        "solved_cases_pct": float(
            recommended_row["solved_cases_pct"]
        ),
        "interpretation": (
            f"The recommended threshold would solve "
            f"{recommended_row['solved_cases_pct']}% of problematic "
            "situations involving late returns."
        ),
    },

    "scope_decision": {
        "question": (
            "Should the feature be enabled for all cars "
            "or only Connect vehicles?"
        ),
        "affected_connect": connect_affected_60,
        "affected_mobile": mobile_affected_60,
        "interpretation": (
            "A significant number of impacted rentals come from both "
            "Connect and Mobile flows. Restricting the feature to "
            "Connect vehicles would leave many problematic situations "
            "unsolved. Therefore the recommended scope is all cars."
        ),
    },
}

executive_summary = {
    "recommended_threshold": 60,
    "recommended_scope": "all_cars",
    "solved_cases_pct": float(
        recommended_row["solved_cases_pct"]
    ),
    "affected_rentals_pct": float(
        recommended_row["affected_rentals_pct"]
    ),
    "key_message": (
        "A 60-minute minimum delay provides the best "
        "trade-off between customer satisfaction and "
        "rental availability."
    )
}

delay_distribution = {
    "median_minutes": round(
        float(
            df_delay["delay_checkout"].quantile(0.50)
        ),
        2
    ),
    "p75_minutes": round(
        float(
            df_delay["delay_checkout"].quantile(0.75)
        ),
        2
    ),
    "p90_minutes": round(
        float(
            df_delay["delay_checkout"].quantile(0.90)
        ),
        2
    ),
    "p95_minutes": round(
        float(
            df_delay["delay_checkout"].quantile(0.95)
        ),
        2
    ),
}

# BUNDLE


bundle = {

    "executive_summary": executive_summary,

    "business_answers": business_answers,

    "summary": {
        "total_rentals": int(len(df)),
        "successive_rentals": int(len(df_chain)),
        "late_driver_rate_pct": late_rate,
        "impacted_next_driver_count": impacted_count,
        "impacted_next_driver_pct": impacted_pct,
        # MOD
        "problematic_cases": problematic_cases,
    },

    "threshold_analysis": threshold_results,

    "connect_vs_mobile": {
        "threshold": 60,
        "affected_connect": connect_affected_60,
        "affected_mobile": mobile_affected_60,
    },

    "delay_distribution": delay_distribution,

    # MOD
    "recommendation": {
        "recommended_threshold": 60,
        "recommended_threshold_hours": 2,
        # MOD
        "scope": "all_cars",
        "solved_cases_pct": float(
            recommended_row["solved_cases_pct"]
        ),
        "affected_rentals_pct": float(
            recommended_row["affected_rentals_pct"]
        ),
        "interpretation": interpretation,
    },

    # MOD
    "figures": {
        "affected_curve": affected_curve,
        "solved_curve": solved_curve,
        "efficiency_curve": efficiency_curve,
        "benefit_slope_curve": benefit_slope_curve,
    },
}


# SAVE


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        bundle,
        f,
        indent=4,
        ensure_ascii=False,
    )

print(
    f"Analytics bundle saved to: {OUTPUT_PATH}"
)