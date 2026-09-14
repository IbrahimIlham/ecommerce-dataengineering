select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    quantity * unit_price AS item_amount
from {{ source('raw', 'order_items') }}