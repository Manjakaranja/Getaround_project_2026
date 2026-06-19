# Getaround Project 2026

## End-to-End Machine Learning Deployment & Decision Support System

This project was completed as part of the **CDSD RNCP Level 6 certification pathway**, specifically within:

**Bloc 5 – Industrialization of Machine Learning Algorithms and Automation of Decision Processes**

The objective was to solve two business challenges proposed by **Getaround**, a peer-to-peer car-sharing platform:

1. **Reduce customer friction caused by late vehicle returns** through data analysis and decision-support dashboards.
2. **Optimize vehicle pricing** using machine learning models deployed as a production-ready API.

The project covers the complete Machine Learning lifecycle:

* Data Analysis
* Business Recommendations
* Feature Engineering
* Model Training & Selection
* Experiment Tracking with MLflow
* Model Deployment with FastAPI
* Dashboard Deployment with Streamlit
* Cloud Storage Integration with AWS S3
* Production Hosting on Hugging Face Spaces

---

# Executive Summary

Late vehicle returns can create significant operational issues when multiple rentals occur on the same day.

To reduce customer dissatisfaction while preserving rental availability, different minimum delay thresholds between consecutive rentals were evaluated.

## Recommended Configuration

| Parameter               | Recommendation |
| ----------------------- | -------------- |
| Minimum delay threshold | **60 minutes** |
| Scope                   | **All Cars**   |

## Expected Outcomes

| Metric                        | Result                   |
| ----------------------------- | ------------------------ |
| Problematic situations solved | **75.11%**               |
| Successive rentals affected   | **21.71%**               |
| Customer friction reduction   | Significant              |
| Business trade-off            | Best operational balance |

This configuration provides the most effective compromise between operational reliability and platform utilization.

---

# Business Context

Getaround allows users to rent vehicles directly from owners for periods ranging from a few hours to several days.

One recurring operational issue is the late return of vehicles. When a rental ends later than expected, the next driver may face delays, cancellations, or poor customer experience.

To address this problem, Getaround considered introducing a mandatory minimum delay between consecutive rentals.

At the same time, the Data Science team was developing a pricing optimization solution to help owners identify appropriate rental prices.

This project therefore combines:

* Business Analytics
* Machine Learning
* Experiment Tracking
* API Deployment
* Dashboard Deployment

within a complete production-oriented workflow.

---

# Technology Stack

## Data Processing

* Python
* Pandas
* NumPy

## Machine Learning

* Scikit-Learn
* Gradient Boosting
* Random Forest
* XGBoost
* RandomizedSearchCV

## Experiment Tracking

* MLflow

## Cloud Storage

* AWS S3
* Boto3

## Backend

* FastAPI
* Uvicorn

## Frontend

* Streamlit
* Plotly

## Deployment

* Docker
* Hugging Face Spaces

## Development Environment

* Jupyter Notebook
* Visual Studio Code

---

# Datasets

Two datasets were provided by Getaround to address distinct business challenges.

## Delay Analysis Dataset

This dataset contains rental lifecycle information used to analyze the impact of late vehicle returns.

Examples of variables include:

* rental_id
* car_id
* checkin_type
* delay_at_checkout_in_minutes
* previous_ended_rental_id
* time_delta_with_previous_rental_in_minutes

### Business Objective

Evaluate how different minimum delay thresholds affect:

* Customer experience
* Rental availability
* Operational efficiency
* Revenue opportunities

---

## Pricing Optimization Dataset

This dataset contains vehicle characteristics and historical rental prices.

Examples of features include:

* model_key
* mileage
* engine_power
* fuel
* car_type
* paint_color
* automatic_car
* has_getaround_connect
* has_gps
* winter_tires
* private_parking_available

### Target Variable

* rental_price_per_day

### Business Objective

Predict optimal vehicle rental prices based on vehicle characteristics.

---

# Project Objectives

The project addresses two complementary business challenges.

## Delay Management

* Quantify the impact of late returns.
* Analyze customer friction.
* Evaluate threshold scenarios.
* Recommend an optimal minimum delay policy.

## Pricing Optimization

* Predict vehicle rental prices.
* Compare machine learning algorithms.
* Select the best production candidate.
* Deploy a prediction API.

## Industrialization

* Track experiments using MLflow.
* Store artifacts in AWS S3.
* Deploy an API using FastAPI.
* Deploy a business dashboard using Streamlit.

---

# Solution Architecture

## Delay Analysis Pipeline

```text
Delay Analysis Notebook
        │
        ▼
analytics_bundle.json
        │
        ▼
AWS S3 Storage
        │
        ▼
Streamlit Dashboard
```

## Pricing Optimization Pipeline

```text
Pricing Dataset
        │
        ▼
Feature Engineering
        │
        ▼
MLflow Experiment Tracking
        │
        ▼
Champion Model Selection
        │
        ▼
FastAPI Prediction Service
        │
        ▼
Hugging Face Deployment
```

---

# Repository Structure

```text
Getaround_project_2026
│
├── data
│   ├── raw
│   └── outputs
│
├── notebook
│   ├── 01_delay_data_clean_analysis.ipynb
│   ├── 02_pricing_data_clean.ipynb
│   └── 03_pricing_modeling.ipynb
│
├── src
│   ├── 01_analytics
│   │   ├── generate_bundle.py
│   │   └── upload_analytics_bundle.py
│   │
│   └── 02_deployment
│       ├── FASTAPI
│       ├── MLFLOW
│       └── STREAMLIT
│
├── requirements.txt
└── README.md
```

---

# Data Preparation Pipeline

## Delay Analysis Pipeline

### Data Validation

The rental dataset was first inspected to evaluate:

* Data quality
* Missing values
* Variable consistency
* Rental relationships

### Data Cleaning

Several preprocessing steps were applied:

* Missing value assessment
* Delay variable validation
* Successive rental reconstruction
* Consistency checks

### Business Feature Engineering

Additional analytical variables were created to support threshold simulations:

* Successive rental indicators
* Problematic rental identification
* Impact metrics
* Threshold evaluation KPIs

---

## Pricing Pipeline

### Data Cleaning

The pricing dataset was prepared through:

* Missing value treatment
* Feature validation
* Data consistency checks

### Feature Engineering

Vehicle characteristics were transformed into machine-learning-ready features.

### Modeling Dataset

The resulting dataset became the final input used for training, evaluation, and deployment.

---

# Delay Analysis

The first part of the project focused on understanding the operational impact of late vehicle returns.

## Key Questions

* How frequently are drivers late?
* How often does a delay impact the next rental?
* What percentage of problematic situations can be prevented?
* What is the business cost of introducing a rental buffer?

## Recommendation

After evaluating multiple thresholds, a **60-minute minimum delay** emerged as the most balanced solution.

### Benefits

* Solves 75.11% of problematic situations

* Affects only 21.71% of successive rentals

* Reduces customer support incidents

* Preserves most rental opportunities

---

# Interactive Dashboard

A Streamlit application was developed to support Product Managers in exploring different business scenarios.

## Features

* Delay distribution analysis
* Operational KPI monitoring
* Threshold impact simulation
* Business recommendation support
* Pricing prediction simulator

## Dashboard Deployment

https://stoneray-streamlit-getaround.hf.space

---

# Analytics Pipeline

To decouple heavy analysis from dashboard rendering:

1. Notebooks generate business KPIs.
2. KPIs are exported as `analytics_bundle.json`.
3. The bundle is uploaded to AWS S3.
4. Streamlit retrieves the latest version directly from S3.

This architecture keeps the dashboard lightweight while maintaining up-to-date analytics.

---

# Pricing Optimization

The second part of the project focuses on predicting optimal vehicle rental prices.

Several machine learning algorithms were trained and compared using MLflow.

---

# Machine Learning Pipeline

## Data Preprocessing

The pricing dataset contains both numerical and categorical vehicle characteristics.

### Numerical Features

Examples:

* mileage
* engine_power

Numerical variables are standardized using:

* StandardScaler

### Categorical Features

Examples:

* model_key
* fuel
* paint_color
* car_type

Categorical variables are encoded using:

* OneHotEncoder(handle_unknown="ignore")

### Unified Pipeline

A Scikit-Learn Pipeline combines preprocessing and model training into a single reusable workflow.

```text
Raw Data
    │
    ▼
ColumnTransformer
 ├── StandardScaler
 └── OneHotEncoder
    │
    ▼
Machine Learning Model
    │
    ▼
Prediction
```

This guarantees identical preprocessing during both training and production inference.

---

# Model Comparison

| Model                     | MAE       | RMSE      | R²        |
| ------------------------- | --------- | --------- | --------- |
| Linear Regression         | 17.53     | 24.95     | 0.470     |
| Random Forest             | 16.69     | 24.51     | 0.489     |
| Gradient Boosting         | 16.88     | 24.16     | 0.503     |
| XGBoost                   | 16.59     | 24.13     | 0.504     |
| **Tune_GradientBoosting** | **16.95** | **23.92** | **0.513** |

---

# Model Evaluation

## Linear Regression

Provided a strong interpretable baseline but struggled to capture nonlinear pricing relationships.

## Random Forest

Improved predictive performance through ensemble learning but remained below the strongest candidates.

## Gradient Boosting

Demonstrated strong predictive capability and became one of the leading models.

## XGBoost

Delivered competitive performance but did not outperform the final selected model.

## Tune_GradientBoosting

Achieved the best overall balance between explanatory power, predictive accuracy, and robustness.

---

# Champion Model

## Tune_GradientBoosting

The tuned Gradient Boosting model was selected as the production model.

### Why Tune_GradientBoosting?

#### Best Pattern Recognition (R² = 0.5132)

The model captures the highest proportion of variance in rental prices, indicating a better understanding of pricing dynamics.

#### Reliable Prediction Accuracy (MAE = 16.95)

The average prediction error remains competitive while maintaining stronger explanatory power.

#### Lowest Severe Error Risk (RMSE = 23.91)

RMSE heavily penalizes large mistakes. The champion model achieves the lowest score, making it the most robust production candidate.

---

# Feature Importance

The most influential variables identified by the champion model are:

| Rank | Feature                   |
| ---- | ------------------------- |
| 1    | model_key                 |
| 2    | automatic_car             |
| 3    | car_type                  |
| 4    | has_getaround_connect     |
| 5    | has_gps                   |
| 6    | paint_color               |
| 7    | winter_tires              |
| 8    | has_speed_regulator       |
| 9    | private_parking_available |
| 10   | fuel                      |

These variables contribute most strongly to rental price estimation.

---

# Key Findings

## Late Returns Generate Significant Operational Friction

A substantial share of customer issues originates from delayed vehicle returns impacting subsequent rentals.

## A 60-Minute Buffer Provides The Best Trade-Off

The selected threshold solves most problematic situations while preserving the majority of rental opportunities.

## Operational Benefits Outweigh Availability Losses

Only a limited share of rentals are affected compared with the large reduction in customer friction.

## Vehicle Characteristics Drive Pricing

Vehicle configuration and equipment significantly influence optimal rental prices.

## Ensemble Models Capture Pricing Dynamics Best

Gradient Boosting methods consistently outperformed simpler linear approaches.

---

# MLflow Experiment Tracking

MLflow was used to:

* Track experiments
* Compare model performances
* Store metrics and parameters
* Manage candidate models
* Select the champion model

## MLflow Deployment

https://stoneray-mlflow-getaround.hf.space

### Artifact Storage

MLflow artifacts are stored in AWS S3, providing persistent storage independent of deployment environments.

---

# FastAPI Prediction Service

The selected model is exposed through a FastAPI application.

## API Deployment

https://stoneray-fastapi-getaround.hf.space

## Prediction Endpoint

### Request

```http
POST /predict
```

Example payload:

```json
{
  "input": [
    [7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]
  ]
}
```

### Response

```json
{
  "prediction": [6]
}
```

---

## Interactive Documentation

https://stoneray-fastapi-getaround.hf.space/docs

---

# Local Installation

```bash
git clone https://github.com/<your-username>/Getaround_project_2026.git

cd Getaround_project_2026

pip install -r requirements.txt
```

---

# AWS Configuration

The analytics bundle and MLflow artifacts rely on AWS S3.

Configure credentials using either environment variables or AWS CLI.

### Environment Variables

```bash
export AWS_ACCESS_KEY_ID=YOUR_KEY
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET
export AWS_DEFAULT_REGION=YOUR_REGION
```

### AWS CLI

```bash
aws configure
```

---

# Run Streamlit

```bash
streamlit run src/02_deployment/STREAMLIT/app.py
```

---

# Run FastAPI

```bash
uvicorn api.main:app --reload
```

---

# Future Improvements

* Automated retraining workflows.
* CI/CD deployment pipelines.
* Model registry promotion workflows.
* Real-time monitoring dashboards.
* Dynamic pricing optimization.
* Demand forecasting models.
* Customer segmentation.
* Production alerting systems.

---
