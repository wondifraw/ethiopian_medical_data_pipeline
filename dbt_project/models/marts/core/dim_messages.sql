{{
  config(
    materialized='table',
    description='Dimension table for Telegram messages.'
  )
}}

select * from {{ ref('stg_telegram_messages') }}