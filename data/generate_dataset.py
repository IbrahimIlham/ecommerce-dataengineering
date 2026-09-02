import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

# Reproducible dataset
random.seed(42)

OUTPUT_DIR = Path(__file__).parent / "source"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NUM_CUSTOMERS = 1_000
NUM_PRODUCTS = 200
NUM_ORDERS = 3_000


def random_date(start_date, end_date):
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))


# -------------------------------------------------------------------
# 1. Customers
# -------------------------------------------------------------------
customers = []

first_names = [
    "Andi", "Budi", "Citra", "Dinda", "Eka",
    "Fajar", "Gita", "Hadi", "Intan", "Joko",
    "Karin", "Lukman", "Maya", "Nanda", "Putri",
    "Rizky", "Sari", "Taufik", "Vina", "Yusuf"
]

last_names = [
    "Pratama", "Saputra", "Wijaya", "Santoso", "Permata",
    "Nugraha", "Hidayat", "Kurniawan", "Lestari", "Ramadhan"
]

cities = [
    "Jakarta", "Bandung", "Depok", "Bekasi", "Bogor",
    "Tangerang", "Surabaya", "Semarang", "Yogyakarta", "Medan"
]

customer_start = datetime(2023, 1, 1)
customer_end = datetime(2025, 12, 31)

for customer_id in range(1, NUM_CUSTOMERS + 1):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    customers.append({
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": f"{first_name.lower()}.{last_name.lower()}{customer_id}@example.com",
        "gender": random.choice(["Male", "Female"]),
        "date_of_birth": random_date(
            datetime(1970, 1, 1),
            datetime(2005, 12, 31)
        ).date(),
        "city": random.choice(cities),
        "created_at": random_date(customer_start, customer_end),
    })

customers_df = pd.DataFrame(customers)


# -------------------------------------------------------------------
# 2. Products
# -------------------------------------------------------------------
products = []

categories = {
    "Electronics": ["Wireless Mouse", "Keyboard", "Headset", "Webcam", "USB Hub"],
    "Fashion": ["T-Shirt", "Hoodie", "Jeans", "Sneakers", "Jacket"],
    "Home": ["Lamp", "Pillow", "Table", "Chair", "Storage Box"],
    "Beauty": ["Face Wash", "Moisturizer", "Shampoo", "Perfume", "Sunscreen"],
    "Sports": ["Running Shoes", "Yoga Mat", "Dumbbell", "Jersey", "Sports Bag"],
}

product_id = 1

for category, product_names in categories.items():
    for name in product_names:
        for variant in range(1, 9):
            if product_id > NUM_PRODUCTS:
                break

            products.append({
                "product_id": product_id,
                "product_name": f"{name} {variant}",
                "category": category,
                "price": round(random.uniform(25_000, 5_000_000), 2),
                "stock_quantity": random.randint(0, 200),
                "created_at": random_date(
                    datetime(2023, 1, 1),
                    datetime(2025, 12, 31)
                ),
            })

            product_id += 1

        if product_id > NUM_PRODUCTS:
            break

    if product_id > NUM_PRODUCTS:
        break

products_df = pd.DataFrame(products)


# -------------------------------------------------------------------
# 3. Orders
# -------------------------------------------------------------------
orders = []

order_statuses = [
    "completed",
    "completed",
    "completed",
    "completed",
    "cancelled",
    "pending",
    "failed",
]

order_start = datetime(2025, 1, 1)
order_end = datetime(2025, 12, 31)

for order_id in range(1, NUM_ORDERS + 1):
    order_date = random_date(order_start, order_end)

    orders.append({
        "order_id": order_id,
        "customer_id": random.randint(1, NUM_CUSTOMERS),
        "order_date": order_date,
        "status": random.choice(order_statuses),
        # Temporary value; will be recalculated after order_items are created.
        "total_amount": 0.0,
    })

orders_df = pd.DataFrame(orders)


# -------------------------------------------------------------------
# 4. Order Items
# -------------------------------------------------------------------
order_items = []
order_item_id = 1

product_prices = products_df.set_index("product_id")["price"].to_dict()

for order_id in range(1, NUM_ORDERS + 1):
    number_of_items = random.randint(1, 4)
    selected_products = random.sample(
        range(1, NUM_PRODUCTS + 1),
        number_of_items
    )

    order_total = 0.0

    for product_id in selected_products:
        quantity = random.randint(1, 5)
        unit_price = product_prices[product_id]

        order_items.append({
            "order_item_id": order_item_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
        })

        order_total += quantity * unit_price
        order_item_id += 1

    orders_df.loc[
        orders_df["order_id"] == order_id,
        "total_amount"
    ] = round(order_total, 2)

order_items_df = pd.DataFrame(order_items)


# -------------------------------------------------------------------
# 5. Payments
# -------------------------------------------------------------------
payments = []

payment_methods = [
    "credit_card",
    "debit_card",
    "bank_transfer",
    "e_wallet",
]

for _, order in orders_df.iterrows():
    if order["status"] == "completed":
        payment_status = "paid"
    elif order["status"] == "cancelled":
        payment_status = random.choice(["refunded", "failed"])
    elif order["status"] == "failed":
        payment_status = "failed"
    else:
        payment_status = "pending"

    payments.append({
        "payment_id": len(payments) + 1,
        "order_id": int(order["order_id"]),
        "payment_date": order["order_date"] + timedelta(
            hours=random.randint(1, 48)
        ),
        "payment_method": random.choice(payment_methods),
        "payment_status": payment_status,
        "amount": order["total_amount"],
    })

payments_df = pd.DataFrame(payments)


# -------------------------------------------------------------------
# Save CSV files
# -------------------------------------------------------------------
datasets = {
    "customers.csv": customers_df,
    "products.csv": products_df,
    "orders.csv": orders_df,
    "order_items.csv": order_items_df,
    "payments.csv": payments_df,
}

for filename, df in datasets.items():
    output_path = OUTPUT_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"Created {output_path} ({len(df):,} rows)")


print("\nDataset generation completed.")
