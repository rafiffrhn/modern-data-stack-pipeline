{{ config(materialized='table') }}

with staging as (
    select * from {{ ref('stg_yellow_strips') }}
)

select
    date(pickup_datetime) as trip_date,
    count(*) as total_trips,
    sum(passenger_count) as total_passengers,
    sum(total_amount) as total_revenue
from staging
group by 1
order by 1 desc