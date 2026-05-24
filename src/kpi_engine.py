import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(PROCESSED_DIR / "supply_chain_master.csv")
inventory = pd.read_csv(PROCESSED_DIR / "inventory_clean.csv")

# -----------------------------
# Executive KPIs
# -----------------------------
total_orders = df["order_id"].nunique()
total_sales = df["sales_amount"].sum()
total_shipping_cost = df["shipping_cost"].sum()
total_gross_margin = df["gross_margin"].sum()

delayed_orders = df[df["is_delayed"] == 1]["order_id"].nunique()
on_time_orders = total_orders - delayed_orders

on_time_delivery_rate = (on_time_orders / total_orders) * 100
delay_rate = (delayed_orders / total_orders) * 100
avg_delay_days = df["delay_days"].mean()
avg_delivery_cycle = df["delivery_cycle_days"].mean()
gross_margin_pct = (total_gross_margin / total_sales) * 100

executive_kpis = pd.DataFrame({
    "metric": [
        "Total Orders",
        "Total Sales",
        "Total Shipping Cost",
        "Total Gross Margin",
        "On-Time Delivery Rate",
        "Delay Rate",
        "Average Delay Days",
        "Average Delivery Cycle Days",
        "Gross Margin %"
    ],
    "value": [
        total_orders,
        round(total_sales, 2),
        round(total_shipping_cost, 2),
        round(total_gross_margin, 2),
        round(on_time_delivery_rate, 2),
        round(delay_rate, 2),
        round(avg_delay_days, 2),
        round(avg_delivery_cycle, 2),
        round(gross_margin_pct, 2)
    ]
})

# -----------------------------
# Warehouse Performance
# -----------------------------
warehouse_kpis = (
    df.groupby(["warehouse_id", "warehouse_name", "warehouse_region"])
    .agg(
        total_orders=("order_id", "nunique"),
        total_sales=("sales_amount", "sum"),
        delay_rate=("is_delayed", "mean"),
        avg_delay_days=("delay_days", "mean"),
        avg_shipping_cost=("shipping_cost", "mean"),
        gross_margin=("gross_margin", "sum")
    )
    .reset_index()
)

warehouse_kpis["delay_rate"] = warehouse_kpis["delay_rate"] * 100
warehouse_kpis = warehouse_kpis.round(2)

# -----------------------------
# Supplier Performance
# -----------------------------
supplier_kpis = (
    df.groupby(["supplier_id", "supplier_name", "supplier_region"])
    .agg(
        total_orders=("order_id", "nunique"),
        total_sales=("sales_amount", "sum"),
        delay_rate=("is_delayed", "mean"),
        avg_delay_days=("delay_days", "mean"),
        supplier_reliability_score=("supplier_reliability_score", "mean")
    )
    .reset_index()
)

supplier_kpis["delay_rate"] = supplier_kpis["delay_rate"] * 100
supplier_kpis = supplier_kpis.round(2)

# -----------------------------
# Product Category Performance
# -----------------------------
category_kpis = (
    df.groupby("product_category")
    .agg(
        total_orders=("order_id", "nunique"),
        total_sales=("sales_amount", "sum"),
        total_quantity=("quantity", "sum"),
        delay_rate=("is_delayed", "mean"),
        gross_margin=("gross_margin", "sum")
    )
    .reset_index()
)

category_kpis["delay_rate"] = category_kpis["delay_rate"] * 100
category_kpis["gross_margin_pct"] = (
    category_kpis["gross_margin"] / category_kpis["total_sales"]
) * 100

category_kpis = category_kpis.round(2)

# -----------------------------
# Inventory Risk
# -----------------------------
inventory_kpis = (
    inventory.groupby("warehouse_id")
    .agg(
        total_inventory_records=("product_id", "count"),
        avg_stock_on_hand=("stock_on_hand", "mean"),
        avg_reorder_point=("reorder_point", "mean"),
        stockout_risk_rate=("stockout_risk", "mean")
    )
    .reset_index()
)

inventory_kpis["stockout_risk_rate"] = inventory_kpis["stockout_risk_rate"] * 100
inventory_kpis = inventory_kpis.round(2)

# -----------------------------
# Monthly Performance
# -----------------------------
monthly_kpis = (
    df.groupby(["order_year", "order_month"])
    .agg(
        total_orders=("order_id", "nunique"),
        total_sales=("sales_amount", "sum"),
        delay_rate=("is_delayed", "mean"),
        avg_delay_days=("delay_days", "mean"),
        gross_margin=("gross_margin", "sum")
    )
    .reset_index()
)

monthly_kpis["delay_rate"] = monthly_kpis["delay_rate"] * 100
monthly_kpis = monthly_kpis.round(2)

# Save reports
executive_kpis.to_csv(REPORTS_DIR / "executive_kpis.csv", index=False)
warehouse_kpis.to_csv(REPORTS_DIR / "warehouse_kpis.csv", index=False)
supplier_kpis.to_csv(REPORTS_DIR / "supplier_kpis.csv", index=False)
category_kpis.to_csv(REPORTS_DIR / "category_kpis.csv", index=False)
inventory_kpis.to_csv(REPORTS_DIR / "inventory_kpis.csv", index=False)
monthly_kpis.to_csv(REPORTS_DIR / "monthly_kpis.csv", index=False)

print("KPI reports created successfully.")
print("Files saved in reports/")
print(executive_kpis)
