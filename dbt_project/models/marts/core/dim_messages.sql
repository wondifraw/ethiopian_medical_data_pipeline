{{
  config(
    materialized='table'
  )
}}

SELECT
    message_key,
    message_id,
    channel_name,
    message_text,
    has_media,
    loaded_at
FROM {{ ref('stg_telegram_messages') }}