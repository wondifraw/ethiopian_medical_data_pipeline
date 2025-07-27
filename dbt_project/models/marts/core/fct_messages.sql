{{
  config(
    materialized='table',
    description='Fact table for Telegram messages.'  -- This table stores all Telegram messages for analytics
  )
}}

select * from {{ ref('stg_telegram_messages') }}  -- Source: staging table for Telegram messages