{{ config(materialized='view') }}

with raw_data as (
    select *
    from {{ source('nyc_taxi_raw', 'yellow_tripdata_2025_12') }}
)

select
    VendorID as vendor_id,
    tpep_pickup_datetime as pickup_datetime,
    tpep_dropoff_datetime as dropoff_datetime,
    passenger_count,
    trip_distance,
    total_amount
from raw_data
where passenger_count > 0
  and total_amount > 0