select
    customer_id,
    first_name,
    last_name,
    TRIM(email) AS email,
    gender,
    date_of_birth,
    city,
    created_at,
    CONCAT(first_name, ' ', last_name) AS full_name
from {{ source('raw', 'customers') }}