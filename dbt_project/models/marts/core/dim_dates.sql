{{
  config(
    materialized='table',
    description='Date dimension for analytics.'  -- This table provides a row for each date to support time-based analysis
  )
}}

select * from calendar_dates  -- Source table containing all calendar dates