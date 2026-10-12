# Modern Data Stack: Automated ELT Pipeline for NYC Taxi Analytics

## Executive Summary
This project demonstrates an enterprise-grade **Modern Data Stack** architecture designed to process high-volume dataset. It features an automated **ELT (Extract, Load, Transform)** pipeline that ingests over 4.3 million rows of NYC Yellow Taxi trip records into a cloud data warehouse, and modularly transforms the raw data into business-ready aggregated metrics. 

By leveraging cloud infrastructure and industry-standard orchestration tools, this pipeline ensures data integrity, eliminates manual processing, and provides optimized datasets for downstream BI dashboards with millisecond latency.

## Architecture & Technology Stack

*   **Cloud Data Warehouse:** **Google Cloud Platform (BigQuery)**
    *   Acts as the highly scalable centralized repository for both raw and transformed data.
*   **Data Transformation:** **dbt (data build tool)**
    *   Applies software engineering principles to data modeling. Handles data cleansing (filtering anomalous fares/passenger counts) and business aggregation via modular SQL.
*   **Pipeline Orchestration:** **Apache Airflow**
    *   Automates the end-to-end ELT lifecycle (scheduled via DAGs), ensuring proper task dependencies and robust failure retries.
*   **Data Ingestion:** **Python (google-cloud-bigquery, pyarrow)**
    *   Efficiently streams highly compressed Parquet data directly from the local environment to the cloud warehouse.

## Data Flow (ELT Process)

1.  **Extract & Load (EL):** The Python ingestion script reads a 4.3 million-row Parquet file (December 2025 NYC Taxi records) and seamlessly loads it into a BigQuery staging dataset (`nyc_taxi_raw`).
2.  **Transform (T):** 
    *   **Staging Layer:** dbt materializes a dynamic `view` (`stg_yellow_trips`) that automatically filters out dirty data (e.g., negative trip distances or zero passenger counts) without duplicating storage.
    *   **Mart Layer:** dbt computes heavy aggregations on the cleaned data, materializing a physical `table` (`mart_daily_revenue`) summarizing daily trips, passenger volume, and total revenue—optimized for immediate BI consumption.
3.  **Orchestrate:** Apache Airflow dictates the execution flow, ensuring the dbt transformation task strictly runs *only after* the ingestion task reports a 100% success rate.

## Repository Structure

```text
├── data/
│   └── raw/
│       └── yellow_tripdata_2025-12.parquet  # Excluded from git via .gitignore
├── src/
│   ├── ingest_to_bq.py                      # Python ingestion script
│   └── taxi_pipeline_dag.py                 # Apache Airflow DAG configuration
├── taxi_transform/                          # dbt project directory
│   ├── models/
│   │   ├── sources.yml                      # dbt source configurations
│   │   ├── stg_yellow_trips.sql             # Staging transformation model
│   │   └── mart_daily_revenue.sql           # Data mart aggregation model
│   ├── dbt_project.yml
│   └── profiles.yml
├── .gitignore
└── README.md
```
## How to Replicate
**1. Prerequisities**
*   Python 3.8+
*   Google Cloud Platform account with an active BigQuery project.
*   A GCP Service Account JSON key (saved as credentials.json in the root folder).
**2. Environment Setup**
Clone this repository and install the required dependencies:
 ```bash
git clone [https://github.com/rafiffrhn/modern-data-stack-pipeline.git](https://github.com/rafiffrhn/modern-data-stack-pipeline.git)
cd modern-data-stack-pipeline
pip install google-cloud-bigquery pyarrow dbt-bigquery apache-airflow
```
**3. Execution (Manual Run)**
* Step 1: Data Ingestion
```bash
python src/ingest_to_bq.py
```
*Expected output: Confirmation of 4.3+ million rows loaded into BigQuery.*
* Step 2: Data Transformation
Navigate to the dbt directory and execute the data models:
```bash
cd taxi_transform
python -m dbt.cli.main run
```
*Expected output: dbt successfully builds the staging view and daily revenue mart table in the cloud.*

**4. Orhestration ((Production Environment)**

To run this pipeline automatically, deploy `src/taxi_pipeline_dag.py` to your Apache Airflow environment (e.g., Google Cloud Composer or a local Dockerized Airflow instance). The DAG is configured to run at midnight daily
