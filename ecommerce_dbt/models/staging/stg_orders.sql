select
    order_id,
    customer_id,
    order_date,
    total_amount,
    status,
    case
        when status = 'completed' then true
        else false
    end as is_completed
from {{ source('raw', 'orders') }}