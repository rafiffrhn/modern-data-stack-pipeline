import os
from google.cloud import bigquery

# 1. Autentikasi menggunakan tiket JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\PROJECT\\modern-data-stack-pipeline\\credentials.json"

client = bigquery.Client()
project_id = client.project

# 2. Membuat Data Warehouse / Dataset baru bernama 'nyc_taxi_raw'
dataset_id = f"{project_id}.nyc_taxi_raw"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"
client.create_dataset(dataset, exists_ok=True)
print(f"1. Dataset '{dataset_id}' berhasil disiapkan di Cloud!")

# 3. Konfigurasi Upload File Parquet berkinerja tinggi
table_id = f"{dataset_id}.yellow_tripdata_2025_12"
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE, 
)

file_path = "D:/PROJECT/modern-data-stack-pipeline/data/raw/yellow_tripdata_2025-12.parquet"

print(f"2. Mengunggah data dari {file_path} ke BigQuery. Harap tunggu...")
with open(file_path, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

job.result()
print(f"3. 🚀 SUKSES! {job.output_rows:,} baris data berhasil mendarat di tabel {table_id}.")