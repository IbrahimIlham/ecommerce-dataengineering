SELECT
    customer_id,
    full_name,
    email,
    gender,
    date_of_birth,
    city,
    created_at

FROM {{ ref('stg_customers') }}