import pandas as pd
import psycopg2

# 1. Read source CSV
df = pd.read_csv("data/source/payments.csv")
df = df.astype(object).where(pd.notnull(df), None)

print(f"Loaded {len(df):,} payments form CSV")

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
    INSERT INTO raw.payments (
        payment_id,
        order_id,
        payment_date,
        payment_method,
        payment_status,
        amount
    )
    VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        (
            row["payment_id"],
            row["order_id"],
            row["payment_date"],
            row["payment_method"],
            row["payment_status"],
            row["amount"]
        )
    )

# 5. Commit transaction
connection.commit()

print(f"Inserted {len(df):,} payments into raw.payments table.")

# 6. Close resources
cursor.close()
connection.close()

print("Connection closed.")