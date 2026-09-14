SELECT
    oi.order_item_id,
    oi.order_id,
    o.customer_id,
    oi.product_id,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price,
    oi.item_amount,
    o.order_date

FROM {{ ref('stg_order_items') }} oi

JOIN {{ ref('stg_orders') }} o
    ON oi.order_id = o.order_id

JOIN {{ ref('stg_products') }} p
    ON oi.product_id = p.product_id