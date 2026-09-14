SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    status

FROM {{ ref('stg_orders') }}