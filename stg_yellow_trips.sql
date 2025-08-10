{{ config(materialized='table') }}

with source_data as (
    select
        VendorID as vendor_id,
        tpep_pickup_datetime as pickup_datetime,
        tpep_dropoff_datetime as dropoff_datetime,
        passenger_count,
        trip_distance,
        RatecodeID as ratecode_id,
        store_and_fwd_flag,
        PULocationID as pu_location_id,
        DOLocationID as do_location_id,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        congestion_surcharge,
        Airport_fee as airport_fee,

        cast(VendorID as TEXT) || '-' ||
        cast(tpep_pickup_datetime as TEXT) || '-' ||
        cast(PULocationID as TEXT) as trip_id_composite,

        current_timestamp as as_loaded_at
    from main."yellow_trips"
)
select *
from source_data
