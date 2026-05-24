import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

n_orders = 50000
n_products = 500
n_customers = 8000
n_suppliers = 80
n_warehouses = 12

order_ids = np.arange(100001, 100001 + n_orders)

products = pd.DataFrame({
    "product_id": np.arange(1, n_products + 1),
    "product_category": np.random.choice(
        ["Electronics", "Furniture", "Office Supplies", "Apparel", "Home Goods"],
        n_products
    ),
    "unit_price": np.round(np.random.uniform(10, 500, n_products), 2),
    "supplier_id": np.random.randint(1, n_suppliers + 1, n_products)
})

suppliers = pd.DataFrame({
    "supplier_id": np.arange(1, n_suppliers + 1),
    "supplier_name": [f"Supplier_{i}" for i in range(1, n_suppliers + 1)],
    "supplier_region": np.random.choice(["West", "East", "South", "Midwest"], n_suppliers),
    "supplier_reliability_score": np.round(np.random.uniform(0.70, 0.98, n_suppliers), 2)
})

warehouses = pd.DataFrame({
    "warehouse_id": np.arange(1, n_warehouses + 1),
    "warehouse_name": [f"Warehouse_{i}" for i in range(1, n_warehouses + 1)],
    "warehouse_region": np.random.choice(["West", "East", "South", "Midwest"], n_warehouses),
    "capacity": np.random.randint(5000, 20000, n_warehouses)
})

customers = pd.DataFrame({
    "customer_id": np.arange(1, n_customers + 1),
    "customer_region": np.random.choice(["West", "East", "South", "Midwest"], n_customers),
    "customer_segment": np.random.choice(["Consumer", "Corporate", "Small Business"], n_customers)
})

orders = pd.DataFrame({
    "order_id": order_ids,
    "customer_id": np.random.randint(1, n_customers + 1, n_orders),
    "product_id": np.random.randint(1, n_products + 1, n_orders),
    "warehouse_id": np.random.randint(1, n_warehouses + 1, n_orders),
    "order_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(
        np.random.randint(0, 365, n_orders), unit="D"
    ),
    "quantity": np.random.randint(1, 10, n_orders),
    "order_priority": np.random.choice(["Low", "Medium", "High", "Critical"], n_orders, p=[0.35, 0.40, 0.20, 0.05])
})

orders = orders.merge(products[["product_id", "unit_price", "supplier_id"]], on="product_id", how="left")
orders["sales_amount"] = np.round(orders["quantity"] * orders["unit_price"], 2)

shipments = orders[["order_id", "warehouse_id", "order_date", "order_priority"]].copy()

shipments["planned_ship_date"] = shipments["order_date"] + pd.to_timedelta(
    np.random.randint(1, 5, n_orders), unit="D"
)

delay_probability = np.where(
    shipments["order_priority"].isin(["High", "Critical"]),
    0.18,
    0.28
)

shipments["is_delayed"] = np.random.binomial(1, delay_probability)

shipments["delay_days"] = np.where(
    shipments["is_delayed"] == 1,
    np.random.randint(1, 10, n_orders),
    0
)

shipments["actual_ship_date"] = shipments["planned_ship_date"] + pd.to_timedelta(
    shipments["delay_days"], unit="D"
)

shipments["shipping_cost"] = np.round(
    np.random.uniform(5, 80, n_orders) + shipments["delay_days"] * np.random.uniform(2, 8, n_orders),
    2
)

inventory = pd.DataFrame({
    "warehouse_id": np.random.randint(1, n_warehouses + 1, 6000),
    "product_id": np.random.randint(1, n_products + 1, 6000),
    "stock_on_hand": np.random.randint(0, 500, 6000),
    "reorder_point": np.random.randint(50, 200, 6000)
})

inventory["stockout_risk"] = np.where(
    inventory["stock_on_hand"] < inventory["reorder_point"],
    1,
    0
)

orders.to_csv(RAW_DIR / "orders.csv", index=False)
shipments.to_csv(RAW_DIR / "shipments.csv", index=False)
products.to_csv(RAW_DIR / "products.csv", index=False)
suppliers.to_csv(RAW_DIR / "suppliers.csv", index=False)
warehouses.to_csv(RAW_DIR / "warehouses.csv", index=False)
customers.to_csv(RAW_DIR / "customers.csv", index=False)
inventory.to_csv(RAW_DIR / "inventory.csv", index=False)

print("Supply chain datasets created successfully.")
print(f"Orders: {orders.shape}")
print(f"Shipments: {shipments.shape}")
print(f"Products: {products.shape}")
print(f"Suppliers: {suppliers.shape}")
print(f"Warehouses: {warehouses.shape}")
print(f"Customers: {customers.shape}")
print(f"Inventory: {inventory.shape}")
