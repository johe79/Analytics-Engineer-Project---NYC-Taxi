import pandas as pd
import os
from datetime import datetime, timedelta

# --- Configuration for Dynamic Month Selection ---
# Get the current date
today = datetime.now()

# Calculate the first day of the current month
first_day_of_current_month = today.replace(day=1)

# Go back two months from the first day of the current month
# This ensures we reliably target data that has likely been released.
# E.g., if today is July 21, 2025:
#   first_day_of_current_month = July 1, 2025
#   last_day_of_two_months_ago = July 1, 2025 - 61 days (approx) = May 1, 2025 (or late April)
#   The year and month from that date will be May 2025.
target_date_two_months_ago = first_day_of_current_month - timedelta(days=61) # Approx 2 months back

YEAR = target_date_two_months_ago.year
MONTH = target_date_two_months_ago.month

# Full URL for the Parquet file (using the CloudFront URL we found)
S3_PATH = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{YEAR:04d}-{MONTH:02d}.parquet"

# Local path to save the data
LOCAL_DATA_DIR = "/usr/local/airflow/data/nyc_taxi"
LOCAL_FILE_PATH = os.path.join(LOCAL_DATA_DIR, f"yellow_tripdata_{YEAR:04d}-{MONTH:02d}.parquet")

print(f"Attempting to ingest data for {YEAR}-{MONTH:02d} from: {S3_PATH}")

try:
    # --- Ingest Data Directly from HTTPS URL to Pandas DataFrame ---
    df_taxi = pd.read_parquet(S3_PATH)

    print(f"Successfully ingested {len(df_taxi)} rows of data.")
    print("First 5 rows of the DataFrame:")
    print(df_taxi.head())

    print("\nDataFrame Info (data types, non-null counts):")
    df_taxi.info()

    # --- Save to local disk ---
    os.makedirs(LOCAL_DATA_DIR, exist_ok=True)
    df_taxi.to_parquet(LOCAL_FILE_PATH, index=False)
    print(f"\nData also saved locally to: {LOCAL_FILE_PATH}")

except Exception as e:
    print(f"An error occurred during data ingestion: {e}")
    print("Ensure you have an active internet connection.")

print("\n--- Data Ingestion Process Complete ---")