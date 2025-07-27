{{ 
  config(
    materialized='table',
    description='Dimension table for Telegram channels.'
  ) 
}}

select
    id as channel_id, -- Unique identifier for each Telegram channel
    name as channel_name, -- The display name of the Telegram channel
    description as channel_description -- Optional: channel description text
from {{ ref('stg_telegram_channels') }}

-- dbt test: unique and not null for channel_id are defined in schema.yml