{{
  config(
    materialized='table',
    description='Fact table for image detections from object detection.'  -- This table stores results of object detection performed on images from Telegram messages
  )
}}

select * from raw_image_detections  -- Source: raw detections from image processing pipeline