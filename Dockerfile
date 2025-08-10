# Extend the official Airflow image
FROM apache/airflow:2.9.2

# Install dbt and its dependencies
# Using specific versions for consistency
RUN pip install --no-cache-dir \
    "dbt-core==1.9.0" \
    "dbt-sqlite==1.9.0" \
    "pendulum" \
    "pandas" \
    "sqlalchemy" \
    "pyarrow"