{{
  config(
    materialized='table',
    description='Dimension table for Telegram messages.'  -- This table contains metadata and attributes for each message
  )
}}

select * from {{ ref('stg_telegram_messages') }}  -- Source: staging table for Telegram messages