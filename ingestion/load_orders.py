import pandas as pd
import psycopg2

# 1. Read source CSV
df = pd.read_csv("data/source/orders.csv")

print(f"Loaded {len(df):,} orders form CSV")

# 2. Connect to PostgreSQL
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="ecommerce_dw",
    user="de_user",
    password="de_password"
)

# 3. Create Cursor
cursor = connection.cursor()

#4. Insert data into Schema RAW
insert_query = """
    INSERT INTO raw.orders (
        order_id,
        customer_id,
        order_date,
        status,
        total_amount
    )
    VALUES (%s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        (
            row["order_id"],
            row["customer_id"],
            row["order_date"],
            row["status"],
            row["total_amount"]
        )
    )

# 5. Commit transaction
connection.commit()

print(f"Inserted {len(df):,} orders into raw.orders table.")

# 6. Close resources
cursor.close()
connection.close()

print("Connection closed.")