import pyarrow.parquet as pq

# Load the Parquet file
table = pq.read_table("yellow_tripdata_2025-05.parquet")

# Print the schema
print(table.schema)