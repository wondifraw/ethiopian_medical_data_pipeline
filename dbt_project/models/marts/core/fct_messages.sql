{{
  config(
    materialized='table',
    description='Fact table for Telegram messages.'
  )
}}

select * from {{ ref('stg_telegram_messages') }}