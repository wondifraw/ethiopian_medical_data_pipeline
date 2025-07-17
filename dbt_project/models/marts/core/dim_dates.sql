{{
  config(
    materialized='table',
    description='Date dimension for analytics.'
  )
}}

select * from calendar_dates