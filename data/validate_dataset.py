import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/source")

# Validasi Source Dataset
for file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(file)

    print(f"\n=== {file.name} ===")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Nulls: {df.isna().sum().sum():,}")
    print(f"Duplicate rows: {df.duplicated().sum():,}")
    print(df.head(3))

## Validasi referential integrity
customers = pd.read_csv(DATA_DIR / "customers.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
order_items = pd.read_csv(DATA_DIR / "order_items.csv")
payments = pd.read_csv(DATA_DIR / "payments.csv")

print("\n=== Referential Integrity ===")

invalid_order_customers = ~orders["customer_id"].isin(
    customers["customer_id"]
)

invalid_item_orders = ~order_items["order_id"].isin(
    orders["order_id"]
)

invalid_item_products = ~order_items["product_id"].isin(
    products["product_id"]
)

invalid_payment_orders = ~payments["order_id"].isin(
    orders["order_id"]
)

print(
    "Invalid orders.customer_id:",
    invalid_order_customers.sum()
)

print(
    "Invalid order_items.order_id:",
    invalid_item_orders.sum()
)

print(
    "Invalid order_items.product_id:",
    invalid_item_products.sum()
)

print(
    "Invalid payments.order_id:",
    invalid_payment_orders.sum()
)
