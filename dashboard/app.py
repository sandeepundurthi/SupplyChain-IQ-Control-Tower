import pandas as pd
import plotly.express as px
import streamlit as st
import joblib
from pathlib import Path

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="SupplyChain IQ",
    page_icon="🚚",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "supply_chain_master.csv"
REPORTS_DIR = BASE_DIR / "reports"
MODEL_PATH = BASE_DIR / "models" / "delay_prediction_model.pkl"
ENCODER_PATH = BASE_DIR / "models" / "label_encoders.pkl"
# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

df = load_data()

@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODER_PATH)
    return model, encoders

model, label_encoders = load_model()
# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.title("Filters")

regions = st.sidebar.multiselect(
    "Warehouse Region",
    options=sorted(df["warehouse_region"].dropna().unique()),
    default=sorted(df["warehouse_region"].dropna().unique())
)

categories = st.sidebar.multiselect(
    "Product Category",
    options=sorted(df["product_category"].dropna().unique()),
    default=sorted(df["product_category"].dropna().unique())
)

priority = st.sidebar.multiselect(
    "Order Priority",
    options=sorted(df["order_priority"].dropna().unique()),
    default=sorted(df["order_priority"].dropna().unique())
)

filtered_df = df[
    (df["warehouse_region"].isin(regions)) &
    (df["product_category"].isin(categories)) &
    (df["order_priority"].isin(priority))
]
tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Dashboard",
    "Warehouse Analytics",
    "AI Predictions",
    "Business Insights"
])
# -----------------------------
# Header
# -----------------------------
st.title("🚚 SupplyChain IQ: AI-Powered Supply Chain Control Tower")
st.write(
    "An end-to-end analytics dashboard for monitoring shipment delays, warehouse performance, "
    "supplier reliability, inventory risk, and operational KPIs."
)

# -----------------------------
# Executive KPIs
# -----------------------------
total_orders = filtered_df["order_id"].nunique()
total_sales = filtered_df["sales_amount"].sum()
total_shipping_cost = filtered_df["shipping_cost"].sum()
gross_margin = filtered_df["gross_margin"].sum()

delay_rate = filtered_df["is_delayed"].mean() * 100
on_time_rate = 100 - delay_rate
avg_delay_days = filtered_df["delay_days"].mean()
avg_delivery_cycle = filtered_df["delivery_cycle_days"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Sales", f"${total_sales:,.0f}")
col3.metric("On-Time Delivery", f"{on_time_rate:.2f}%")
col4.metric("Delay Rate", f"{delay_rate:.2f}%")

col5, col6, col7, col8 = st.columns(4)

col5.metric("Avg Delay Days", f"{avg_delay_days:.2f}")
col6.metric("Avg Delivery Cycle", f"{avg_delivery_cycle:.2f} days")
col7.metric("Shipping Cost", f"${total_shipping_cost:,.0f}")
col8.metric("Gross Margin", f"${gross_margin:,.0f}")

st.divider()

# -----------------------------
# Monthly performance
# -----------------------------
st.subheader("Monthly Sales and Delay Trends")

monthly = (
    filtered_df.groupby(["order_year", "order_month"])
    .agg(
        total_sales=("sales_amount", "sum"),
        delay_rate=("is_delayed", "mean"),
        avg_delay_days=("delay_days", "mean"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

monthly["delay_rate"] = monthly["delay_rate"] * 100
monthly["month_label"] = monthly["order_year"].astype(str) + "-" + monthly["order_month"].astype(str).str.zfill(2)

fig_sales = px.line(
    monthly,
    x="month_label",
    y="total_sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig_sales, use_container_width=True)

fig_delay = px.line(
    monthly,
    x="month_label",
    y="delay_rate",
    markers=True,
    title="Monthly Delay Rate Trend"
)

st.plotly_chart(fig_delay, use_container_width=True)

st.divider()

# -----------------------------
# Warehouse performance
# -----------------------------
st.subheader("Warehouse Performance")

warehouse_perf = (
    filtered_df.groupby(["warehouse_name", "warehouse_region"])
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

warehouse_perf["delay_rate"] = warehouse_perf["delay_rate"] * 100
warehouse_perf = warehouse_perf.round(2)

fig_warehouse = px.bar(
    warehouse_perf.sort_values("delay_rate", ascending=False),
    x="warehouse_name",
    y="delay_rate",
    color="warehouse_region",
    title="Delay Rate by Warehouse"
)

st.plotly_chart(fig_warehouse, use_container_width=True)

st.dataframe(
    warehouse_perf.sort_values("delay_rate", ascending=False),
    use_container_width=True
)

st.divider()

# -----------------------------
# Supplier scorecard
# -----------------------------
st.subheader("Supplier Reliability Scorecard")

supplier_perf = (
    filtered_df.groupby(["supplier_name", "supplier_region"])
    .agg(
        total_orders=("order_id", "nunique"),
        total_sales=("sales_amount", "sum"),
        delay_rate=("is_delayed", "mean"),
        avg_delay_days=("delay_days", "mean"),
        reliability_score=("supplier_reliability_score", "mean")
    )
    .reset_index()
)

supplier_perf["delay_rate"] = supplier_perf["delay_rate"] * 100
supplier_perf = supplier_perf.round(2)

fig_supplier = px.scatter(
    supplier_perf,
    x="reliability_score",
    y="delay_rate",
    size="total_orders",
    color="supplier_region",
    hover_name="supplier_name",
    title="Supplier Reliability vs Delay Rate"
)

st.plotly_chart(fig_supplier, use_container_width=True)

st.dataframe(
    supplier_perf.sort_values("delay_rate", ascending=False).head(20),
    use_container_width=True
)

st.divider()

# -----------------------------
# Product category performance
# -----------------------------
st.subheader("Product Category Performance")

category_perf = (
    filtered_df.groupby("product_category")
    .agg(
        total_orders=("order_id", "nunique"),
        total_sales=("sales_amount", "sum"),
        total_quantity=("quantity", "sum"),
        delay_rate=("is_delayed", "mean"),
        gross_margin=("gross_margin", "sum")
    )
    .reset_index()
)

category_perf["delay_rate"] = category_perf["delay_rate"] * 100
category_perf["gross_margin_pct"] = (
    category_perf["gross_margin"] / category_perf["total_sales"]
) * 100

category_perf = category_perf.round(2)

fig_category = px.bar(
    category_perf.sort_values("total_sales", ascending=False),
    x="product_category",
    y="total_sales",
    title="Sales by Product Category"
)

st.plotly_chart(fig_category, use_container_width=True)

st.dataframe(category_perf, use_container_width=True)

st.divider()

# -----------------------------
# High-risk shipments
# -----------------------------
st.subheader("High-Risk Shipments")

high_risk = filtered_df[
    filtered_df["risk_level"].isin(["Medium Risk", "High Risk"])
][
    [
        "order_id",
        "order_date",
        "warehouse_name",
        "warehouse_region",
        "supplier_name",
        "product_category",
        "order_priority",
        "sales_amount",
        "delay_days",
        "risk_level"
    ]
].sort_values("delay_days", ascending=False)

st.dataframe(high_risk.head(50), use_container_width=True)

st.divider()
st.subheader("AI Shipment Delay Prediction")

st.write(
    "Use this tool to predict whether a shipment is likely to be delayed based on operational inputs."
)

col1, col2, col3 = st.columns(3)

with col1:
    input_warehouse_region = st.selectbox(
        "Warehouse Region",
        sorted(df["warehouse_region"].dropna().unique())
    )

    input_product_category = st.selectbox(
        "Product Category",
        sorted(df["product_category"].dropna().unique())
    )

    input_customer_region = st.selectbox(
        "Customer Region",
        sorted(df["customer_region"].dropna().unique())
    )

with col2:
    input_customer_segment = st.selectbox(
        "Customer Segment",
        sorted(df["customer_segment"].dropna().unique())
    )

    input_order_priority = st.selectbox(
        "Order Priority",
        sorted(df["order_priority"].dropna().unique())
    )

    input_quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=20,
        value=5
    )

with col3:
    input_sales_amount = st.number_input(
        "Sales Amount",
        min_value=1.0,
        value=500.0
    )

    input_shipping_cost = st.number_input(
        "Shipping Cost",
        min_value=1.0,
        value=50.0
    )

    input_supplier_reliability = st.slider(
        "Supplier Reliability Score",
        min_value=0.70,
        max_value=0.98,
        value=0.85,
        step=0.01
    )

if st.button("Predict Delay Risk"):
    input_data = pd.DataFrame([{
        "warehouse_region": input_warehouse_region,
        "product_category": input_product_category,
        "customer_region": input_customer_region,
        "customer_segment": input_customer_segment,
        "order_priority": input_order_priority,
        "quantity": input_quantity,
        "sales_amount": input_sales_amount,
        "shipping_cost": input_shipping_cost,
        "supplier_reliability_score": input_supplier_reliability
    }])

    categorical_cols = [
        "warehouse_region",
        "product_category",
        "customer_region",
        "customer_segment",
        "order_priority"
    ]

    for col in categorical_cols:
        input_data[col] = label_encoders[col].transform(input_data[col])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] * 100

    if probability >= 70:
        risk_level = "High Risk"
    elif probability >= 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    if prediction == 1:
        st.error(f"Prediction: Shipment is likely to be delayed — {probability:.2f}% delay probability")
    else:
        st.success(f"Prediction: Shipment is likely to be on time — {probability:.2f}% delay probability")

    st.info(f"Operational Risk Level: {risk_level}")

    if risk_level == "High Risk":
        st.write("""
        Recommended Action:
        - Prioritize this shipment for monitoring.
        - Contact warehouse operations team.
        - Review supplier reliability and shipping cost.
        - Consider proactive customer communication.
        """)
    elif risk_level == "Medium Risk":
        st.write("""
        Recommended Action:
        - Monitor shipment status closely.
        - Check warehouse workload and supplier performance.
        - Prepare backup shipping options if needed.
        """)
    else:
        st.write("""
        Recommended Action:
        - Shipment appears operationally stable.
        - Continue standard tracking.
        """)
# -----------------------------
# Business insights
# -----------------------------
st.divider()
st.subheader("Business Insights")

top_delay_warehouse = warehouse_perf.sort_values("delay_rate", ascending=False).iloc[0]
top_delay_supplier = supplier_perf.sort_values("delay_rate", ascending=False).iloc[0]
top_sales_category = category_perf.sort_values("total_sales", ascending=False).iloc[0]

st.write(f"""
### Key Findings

1. **{top_delay_warehouse['warehouse_name']}** has the highest warehouse delay rate at **{top_delay_warehouse['delay_rate']:.2f}%**.
2. **{top_delay_supplier['supplier_name']}** has the highest supplier-related delay rate at **{top_delay_supplier['delay_rate']:.2f}%**.
3. **{top_sales_category['product_category']}** is the highest revenue-generating category with **${top_sales_category['total_sales']:,.0f}** in sales.
4. Overall on-time delivery rate is **{on_time_rate:.2f}%**, meaning operational improvement should focus on delayed shipment clusters.
""")

st.write("""
### Recommended Actions

- Review warehouse staffing and processing capacity for high-delay warehouses.
- Monitor suppliers with high delay rates and low reliability scores.
- Prioritize inventory planning for high-demand product categories.
- Use delay-risk shipments to trigger proactive customer communication.
""")
