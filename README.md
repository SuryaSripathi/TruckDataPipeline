# Real-Time IoT Fleet Telemetry & Predictive Maintenance Pipeline

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![License](https://img.shields.io/badge/License-MIT-green)

![Dashboard Demo](dashboard_demo.png)

## 📌 Project Overview
**End-to-End Data Engineering & Data Science Solution** designed to ingest, process, and analyze real-time telemetry data from a simulated fleet of IoT delivery vehicles.

The system acts as a "Digital Twin" for a logistics fleet, utilizing **Time-Series Forecasting (SARIMAX)** to predict engine failures before they occur, reducing potential downtime. It demonstrates a full-stack data pipeline from raw sensor data generation to actionable predictive insights.

## 🏗 Architecture
The pipeline follows a modern **Producer-Consumer** architecture, containerized for scalability.

## 🚀 How to Run Locally
1. Start the Infrastructure \
docker compose up -d
2. Initialize Database \
python init_db.py
3. Start the Data Pipeline \
python -u data_generator.py | python consumer.py
4. Launch Dashboard \
streamlit run dashboard.py

```mermaid
graph LR
    A[IoT Sensor Simulation] -->|JSON Stream| B(Data Ingestion/ETL)
    B -->|Batch Insert| C[(PostgreSQL DB)]
    C -->|Read History| D[SARIMAX Model]
    C -->|Live Feed| E[Streamlit Dashboard]
    D -->|Alerts| E

├── config.py             # Global configuration (DB credentials, Constants)
├── consumer.py           # ETL Consumer: Ingests stream -> writes to Postgres
├── dashboard.py          # Streamlit frontend for visualization
├── data_generator.py     # IoT Device Simulator (Producer)
├── docker-compose.yml    # Container orchestration for PostgreSQL
├── init_db.py            # Database schema initialization
├── model_analytics.py    # ML Training & Prediction logic
└── requirements.txt      # Python dependencies


