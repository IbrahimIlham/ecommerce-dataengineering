select
    product_id,
    product_name,
    category,
    price,
    stock_quantity,
    created_at,
    case
        when stock_quantity > 0 then true
        else false
    end as is_in_stock
from {{ source('raw', 'products') }}