import pandas as pd
import psycopg2

# 1. Read source CSV
df = pd.read_csv("data/source/order_items.csv")
df = df.astype(object).where(pd.notnull(df), None)

print(f"Loaded {len(df):,} order_items form CSV")

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
    INSERT INTO raw.order_items (
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price
    )
    VALUES (%s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        (
            row["order_item_id"],
            row["order_id"],
            row["product_id"],
            row["quantity"],
            row["unit_price"]
        )
    )

# 5. Commit transaction
connection.commit()

print(f"Inserted {len(df):,} order_items into raw.order_items table.")

# 6. Close resources
cursor.close()
connection.close()

print("Connection closed.")