{{
  config(
    materialized='table',
    description='Dimension table for Telegram channels.'
  )
}}

select
    id as channel_id,
    name as channel_name,
    description as channel_description
from {{ ref('stg_telegram_channels') }}

-- dbt test: unique and not null
-- in dbt_project/models/marts/core/schema.yml