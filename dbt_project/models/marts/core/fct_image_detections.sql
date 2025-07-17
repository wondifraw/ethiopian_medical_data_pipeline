{{
  config(
    materialized='table',
    description='Fact table for image detections from object detection.'
  )
}}

select * from raw_image_detections