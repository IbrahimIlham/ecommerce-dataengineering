import pandas as pd
import psycopg2

# 1. Read source CSV
df = pd.read_csv("data/source/products.csv")

print(f"Loaded {len(df):,} products form CSV")

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
    INSERT INTO raw.products (
        product_id,
        product_name,
        category,
        price,
        stock_quantity,
        created_at
    )
    VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        (
            row["product_id"],
            row["product_name"],
            row["category"],
            row["price"],
            row["stock_quantity"],
            row["created_at"]
        )
    )

# 5. Commit transaction
connection.commit()

print(f"Inserted {len(df):,} products into raw.products table.")

# 6. Close resources
cursor.close()
connection.close()

print("Connection closed.")

