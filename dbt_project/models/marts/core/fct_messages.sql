{{
  config(
    materialized='table'
  )
}}

SELECT
    m.message_key,
    c.channel_key,
    d.date AS date_key,
    m.message_date,
    m.views,
    m.forwards,
    m.has_media,
    m.loaded_at
FROM {{ ref('dim_messages') }} m
JOIN {{ ref('dim_channels') }} c ON m.channel_name = c.channel_name
JOIN {{ ref('dim_dates') }} d ON m.message_date::date = d.date