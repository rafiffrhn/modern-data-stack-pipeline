from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# 1. Konfigurasi Standar Airflow
default_args = {
    'owner': 'rafif_data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 1), 
    'retries': 1,                        
    'retry_delay': timedelta(minutes=5), 
}

# 2. Mendefinisikan DAG (Directed Acyclic Graph)
with DAG(
    'nyc_taxi_modern_data_stack',
    default_args=default_args,
    description='Pipeline otomatis ELT untuk data NYC Taxi',
    schedule_interval='0 0 * * *', 
    catchup=False,
) as dag:

    # TASK 1: Extract & Load (Menjalankan Python Ingestion)
    ingest_raw_data = BashOperator(
        task_id='ingest_to_bigquery',
        bash_command='python D:/PROJECT/modern-data-stack-pipeline/src/ingest_to_bq.py',
    )

    # TASK 2: Transformasi Data (Menjalankan dbt run)
    transform_data_mart = BashOperator(
        task_id='run_dbt_transformations',
        # Masuk ke folder dbt, lalu jalankan run
        bash_command='cd D:/PROJECT/modern-data-stack-pipeline/taxi_transform && py -m dbt.cli.main run',
    )

    # 3. MENGATUR URUTAN (DEPENDENCIES)
    ingest_raw_data >> transform_data_mart