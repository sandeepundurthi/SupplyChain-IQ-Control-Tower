import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load raw files
orders = pd.read_csv(RAW_DIR / "orders.csv")
shipments = pd.read_csv(RAW_DIR / "shipments.csv")
products = pd.read_csv(RAW_DIR / "products.csv")
suppliers = pd.read_csv(RAW_DIR / "suppliers.csv")
warehouses = pd.read_csv(RAW_DIR / "warehouses.csv")
customers = pd.read_csv(RAW_DIR / "customers.csv")
inventory = pd.read_csv(RAW_DIR / "inventory.csv")

# Convert dates
orders["order_date"] = pd.to_datetime(orders["order_date"])
shipments["planned_ship_date"] = pd.to_datetime(shipments["planned_ship_date"])
shipments["actual_ship_date"] = pd.to_datetime(shipments["actual_ship_date"])

# Remove duplicates
orders = orders.drop_duplicates()
shipments = shipments.drop_duplicates()
products = products.drop_duplicates()
suppliers = suppliers.drop_duplicates()
warehouses = warehouses.drop_duplicates()
customers = customers.drop_duplicates()
inventory = inventory.drop_duplicates()

# Create master analytics table
df = orders.merge(
    shipments[["order_id", "planned_ship_date", "actual_ship_date", "is_delayed", "delay_days", "shipping_cost"]],
    on="order_id",
    how="left"
)

df = df.merge(products[["product_id", "product_category"]], on="product_id", how="left")
df = df.merge(customers, on="customer_id", how="left")
df = df.merge(warehouses, on="warehouse_id", how="left")
df = df.merge(suppliers, on="supplier_id", how="left")

# Feature engineering
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month
df["order_month_name"] = df["order_date"].dt.month_name()
df["order_weekday"] = df["order_date"].dt.day_name()

df["delivery_cycle_days"] = (
    df["actual_ship_date"] - df["order_date"]
).dt.days

df["gross_margin"] = df["sales_amount"] - df["shipping_cost"]
df["gross_margin_pct"] = (df["gross_margin"] / df["sales_amount"]) * 100

df["delay_status"] = df["is_delayed"].map({
    0: "On Time",
    1: "Delayed"
})

df["risk_level"] = pd.cut(
    df["delay_days"],
    bins=[-1, 0, 3, 6, 100],
    labels=["No Delay", "Low Risk", "Medium Risk", "High Risk"]
)

# Save cleaned files
df.to_csv(PROCESSED_DIR / "supply_chain_master.csv", index=False)
orders.to_csv(PROCESSED_DIR / "orders_clean.csv", index=False)
shipments.to_csv(PROCESSED_DIR / "shipments_clean.csv", index=False)
inventory.to_csv(PROCESSED_DIR / "inventory_clean.csv", index=False)

print("Cleaned data saved successfully.")
print("Master table shape:", df.shape)
print("Files saved in data/processed/")
