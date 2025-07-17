{{
  config(
    materialized='view'
  )
}}

SELECT
    {{ dbt_utils.generate_surrogate_key(['id', 'channel_name']) }} AS message_key,
    id AS message_id,
    channel_name,
    date::timestamp AS message_date,
    message AS message_text,
    views,
    forwards,
    media AS has_media,
    scraped_date,
    CURRENT_TIMESTAMP AS loaded_at
FROM {{ source('raw', 'raw_telegram_messages') }}