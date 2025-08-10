SELECT *,
derived_key AS (CONCAT(dropoff_datetime, '-', trip_distance, '-', passenger_count, 
'-', ratecode_id, '-', payment_type)) PERSISTED,
    PRIMARY KEY (derived_key)
FROM {{ ref('stg_yellow_trips') }}
WHERE ratecode_id BETWEEN 1 AND 6
  AND passenger_count IS NOT NULL
  AND passenger_count != 0

