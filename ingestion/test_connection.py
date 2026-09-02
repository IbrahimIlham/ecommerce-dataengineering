import psycopg2

connection = psycopg2.connect(
    host="127.0.0.1",
    port=5432,
    database="ecommerce_dw",
    user="de_user",
    password="de_password"
)

print("Successfully connected to PostgreSQL!")

connection.close()
print("Connection closed.")