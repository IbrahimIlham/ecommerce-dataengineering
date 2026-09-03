import pandas as pd
import psycopg2

# 1. Read source CSV
df = pd.read_csv("data/source/customers.csv")
df = df.astype(object).where(pd.notnull(df), None)

print(f"Loaded {len(df):,} customer form CSV")

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
    INSERT INTO raw.customers (
        customer_id,
        first_name,
        last_name,
        email,
        gender,
        date_of_birth,
        city,
        created_at
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        (
            row["customer_id"],
            row["first_name"],
            row["last_name"],
            row["email"],
            row["gender"],
            row["date_of_birth"],
            row["city"],
            row["created_at"]
        )
    )

# 5. Commit transaction
connection.commit()

print(f"Inserted {len(df):,} customers into raw.customers table.")

# 6. Close resources
cursor.close()
connection.close()

print("Connection closed.")

