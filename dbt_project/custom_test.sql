-- tests/test_price_positive.sql
SELECT *
FROM {{ ref('stg_product_prices') }}
WHERE price <= 0;
