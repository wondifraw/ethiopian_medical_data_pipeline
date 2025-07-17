{{
  config(
    materialized='view'
  )
}}

WITH source AS (
    SELECT
        channel_name,
        MIN(date) AS first_seen_date,
        COUNT(*) AS message_count
    FROM {{ source('raw', 'raw_telegram_messages') }}
    GROUP BY channel_name
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['channel_name']) }} AS channel_key,
    channel_name,
    first_seen_date,
    message_count,
    CURRENT_TIMESTAMP AS loaded_at
FROM source