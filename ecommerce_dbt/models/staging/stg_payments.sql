select
    payment_id,
    order_id,
    payment_date,
    payment_method,
    payment_status,
    amount
from {{ source('raw', 'payments') }}