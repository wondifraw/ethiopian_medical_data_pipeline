{{
  config(
    materialized='table'
  )
}}

SELECT
    channel_key,
    channel_name,
    first_seen_date,
    message_count,
    loaded_at
FROM {{ ref('stg_telegram_channels') }}