SELECT
    order_item_id,
    quantity,
    unit_price,
    item_amount
FROM {{ ref('fact_order_items') }}
WHERE item_amount <> quantity * unit_price