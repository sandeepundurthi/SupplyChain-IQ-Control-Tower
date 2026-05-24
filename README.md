# 🚚 SupplyChain IQ: AI-Powered Supply Chain Control Tower

## Overview

SupplyChain IQ is an end-to-end operational intelligence platform designed to monitor shipment delays, warehouse efficiency, supplier reliability, inventory risks, and logistics KPIs using analytics dashboards and machine learning.

The platform combines:
- Data Engineering
- SQL Analytics
- Business Intelligence
- Predictive Analytics
- Operational Risk Monitoring

to support supply chain decision-making.

---

# Business Problem

Modern supply chain operations face challenges such as:
- shipment delays
- warehouse bottlenecks
- supplier reliability issues
- inventory shortages
- operational inefficiencies

This project helps operations teams proactively identify and mitigate logistics risks using data-driven insights and AI-powered delay prediction.

---

# Features

## Executive KPI Dashboard
- Total Orders
- Total Sales
- Gross Margin
- On-Time Delivery Rate
- Shipping Costs
- Delay Rate

## Warehouse Analytics
- Delay rate by warehouse
- Warehouse performance ranking
- Regional operational analysis

## Supplier Intelligence
- Supplier reliability scorecard
- Delay risk monitoring
- Supplier performance comparison

## Product Analytics
- Product category profitability
- Demand analysis
- Operational sales trends

## High-Risk Shipment Monitoring
- Delay risk identification
- Critical shipment tracking
- Operational alerting

## AI Delay Prediction
Machine learning model predicts shipment delays using:
- warehouse region
- supplier reliability
- shipping cost
- order priority
- product category
- customer segment

---

# Tech Stack

## Programming
- Python

## Data Analysis
- Pandas
- NumPy

## Machine Learning
- Scikit-learn
- Random Forest

## Dashboarding
- Streamlit
- Plotly

## Database & SQL
- SQLite
- SQL Analytics

---

# Project Architecture

```text
Raw Data
   ↓
ETL Pipeline
   ↓
Cleaned Analytics Tables
   ↓
SQL KPI Engine
   ↓
Streamlit Dashboard
   ↓
Machine Learning Prediction Layer
   ↓
Operational Business Insights
```

---

# Machine Learning Model

## Objective
Predict whether a shipment is likely to be delayed.

## Model Used
Random Forest Classifier

## Model Performance

| Metric | Score |
|---|---|
| Accuracy | 77.95% |
| Delayed Shipment Recall | 46% |

The model was optimized for operational risk detection rather than raw accuracy to improve delayed shipment identification.

---

# Key Business Insights

- Warehouse_9 had the highest operational delay rate.
- Supplier_69 showed elevated supplier-related delay risk.
- Apparel generated the highest overall sales volume.
- Operational improvements should prioritize delayed shipment clusters and supplier risk management.

---

# Screenshots

## Executive Dashboard
<img width="1440" height="777" alt="Screenshot 2026-05-24 at 00 23 23" src="https://github.com/user-attachments/assets/f36af9b7-16da-4bdd-89f3-0279c3e2200f" />
<img width="1440" height="778" alt="Screenshot 2026-05-24 at 00 23 39" src="https://github.com/user-attachments/assets/57d650d7-97d8-4db6-aff2-44df50e8a681" />
<img width="1440" height="772" alt="Screenshot 2026-05-24 at 00 23 55" src="https://github.com/user-attachments/assets/7924c73a-4429-409c-9744-c5c6b06bed54" />


---

# Installation

## Clone Repository

```bash
git clone <your-github-repo>
cd supplychain-control-tower
```

## Create Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

# Future Improvements

- Real-time streaming analytics
- SHAP explainability
- Geographic shipment heatmaps
- AI chatbot assistant
- Cloud deployment
- PostgreSQL warehouse integration

---

# Author

Sandeep Undurthi
