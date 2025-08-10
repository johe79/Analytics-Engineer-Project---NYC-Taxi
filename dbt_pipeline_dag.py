import os
import sqlite3
import pandas as pd
import pyarrow.parquet as pq
from airflow.decorators import dag, task
from datetime import datetime
from airflow.operators.bash import BashOperator

# Define paths
DATA_DIR = '/opt/airflow/data/nyc_taxi'
DB_DIR = '/opt/airflow/nyc_taxi_dbt/db'
DB_FILE = os.path.join(DB_DIR, 'nyc_taxi.db')
DBT_PROJECT_DIR = '/opt/airflow/nyc_taxi_dbt'
DATA_DB_PATH = '/opt/airflow/nyc_taxi_dbt/db/nyc_taxi.db'

@dag(
    dag_id='nyc_taxi_dbt_pipeline',
    start_date=datetime(2025, 5, 1),
    schedule_interval=None,
    catchup=False,
    tags=['dbt', 'nyc_taxi', 'sqlite'],
)
def nyc_taxi_dbt_pipeline():

    @task
    def load_parquet_to_sqlite_task():
        os.makedirs(DB_DIR, exist_ok=True)
        print(f"Database directory already exists: {DB_DIR}")

        parquet_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.parquet')]
        if not parquet_files:
            raise FileNotFoundError(f"No parquet files found in {DATA_DIR}")
        print(f"Found {len(parquet_files)} parquet files: {parquet_files}")

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        table_name = "yellow_trips"
        print(f"Dropped existing table main.{table_name} (if any).")
        cursor.execute(f"DROP TABLE IF EXISTS main.{table_name};")
        conn.commit()

        for i, file_name in enumerate(parquet_files):
            file_path = os.path.join(DATA_DIR, file_name)
            print(f"Processing file {i+1}/{len(parquet_files)}: {file_path}")

            parquet_file = pq.ParquetFile(file_path)
            for row_group_index in range(parquet_file.num_row_groups):
                table = parquet_file.read_row_group(row_group_index)
                chunk_df = table.to_pandas()
                chunk_df.to_sql(table_name, conn, if_exists='append', index=False)
                print(f"  Appended a chunk (row group {row_group_index}) of {len(chunk_df)} rows to {table_name}")

        conn.close()
        print(f"All parquet files loaded to SQLite table main.{table_name}")

    run_dbt_models = BashOperator(
        task_id='run_dbt_models',
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run",

    )

    # Define task dependencies
    load_parquet_to_sqlite_task() >> run_dbt_models

nyc_taxi_dbt_pipeline()