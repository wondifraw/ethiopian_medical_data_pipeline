{{
  config(
    materialized='table'
  )
}}

WITH messages AS (
    SELECT 
        message_key,
        message_id,
        channel_name
    FROM {{ ref('dim_messages') }}
),

detections AS (
    SELECT
        channel_name,
        message_id,
        object_class,
        confidence,
        image_path
    FROM {{ source('raw', 'raw_image_detections') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['d.channel_name', 'd.message_id', 'd.object_class']) }} AS detection_key,
    m.message_key,
    d.object_class,
    d.confidence,
    d.image_path,
    CURRENT_TIMESTAMP AS loaded_at
FROM detections d
JOIN messages m ON d.channel_name = m.channel_name AND d.message_id::text = m.message_id::text