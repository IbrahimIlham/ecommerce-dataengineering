SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_items,
    SUM(item_amount) AS total_revenue
FROM {{ ref('fact_order_items') }}
GROUP BY customer_id