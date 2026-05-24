-- 1. Executive KPIs
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(SUM(shipping_cost), 2) AS total_shipping_cost,
    ROUND(SUM(gross_margin), 2) AS total_gross_margin,
    ROUND(100.0 * SUM(CASE WHEN is_delayed = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS on_time_delivery_rate,
    ROUND(100.0 * SUM(CASE WHEN is_delayed = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS delay_rate,
    ROUND(AVG(delay_days), 2) AS avg_delay_days
FROM supply_chain_master;


-- 2. Warehouse Delay Performance
SELECT
    warehouse_name,
    warehouse_region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(100.0 * AVG(is_delayed), 2) AS delay_rate,
    ROUND(AVG(delay_days), 2) AS avg_delay_days,
    ROUND(SUM(gross_margin), 2) AS gross_margin
FROM supply_chain_master
GROUP BY warehouse_name, warehouse_region
ORDER BY delay_rate DESC;


-- 3. Supplier Reliability Scorecard
SELECT
    supplier_name,
    supplier_region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(supplier_reliability_score), 2) AS reliability_score,
    ROUND(100.0 * AVG(is_delayed), 2) AS delay_rate,
    ROUND(AVG(delay_days), 2) AS avg_delay_days
FROM supply_chain_master
GROUP BY supplier_name, supplier_region
ORDER BY delay_rate DESC;


-- 4. Product Category Profitability
SELECT
    product_category,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(SUM(gross_margin), 2) AS gross_margin,
    ROUND(100.0 * SUM(gross_margin) / SUM(sales_amount), 2) AS gross_margin_pct,
    ROUND(100.0 * AVG(is_delayed), 2) AS delay_rate
FROM supply_chain_master
GROUP BY product_category
ORDER BY gross_margin DESC;


-- 5. Monthly Trend Analysis
SELECT
    order_year,
    order_month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(100.0 * AVG(is_delayed), 2) AS delay_rate,
    ROUND(AVG(delay_days), 2) AS avg_delay_days,
    ROUND(SUM(gross_margin), 2) AS gross_margin
FROM supply_chain_master
GROUP BY order_year, order_month
ORDER BY order_year, order_month;


-- 6. High-Risk Shipments
SELECT
    order_id,
    order_date,
    warehouse_name,
    warehouse_region,
    supplier_name,
    product_category,
    order_priority,
    sales_amount,
    delay_days,
    risk_level
FROM supply_chain_master
WHERE risk_level IN ('Medium Risk', 'High Risk')
ORDER BY delay_days DESC
LIMIT 50;


-- 7. Window Function: Rank Warehouses by Delay Rate
WITH warehouse_perf AS (
    SELECT
        warehouse_name,
        warehouse_region,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(100.0 * AVG(is_delayed), 2) AS delay_rate,
        ROUND(AVG(delay_days), 2) AS avg_delay_days
    FROM supply_chain_master
    GROUP BY warehouse_name, warehouse_region
)
SELECT
    warehouse_name,
    warehouse_region,
    total_orders,
    delay_rate,
    avg_delay_days,
    RANK() OVER (ORDER BY delay_rate DESC) AS delay_rank
FROM warehouse_perf;


-- 8. Inventory Stockout Risk
SELECT
    warehouse_id,
    COUNT(product_id) AS inventory_records,
    ROUND(AVG(stock_on_hand), 2) AS avg_stock_on_hand,
    ROUND(AVG(reorder_point), 2) AS avg_reorder_point,
    ROUND(100.0 * AVG(stockout_risk), 2) AS stockout_risk_rate
FROM inventory
GROUP BY warehouse_id
ORDER BY stockout_risk_rate DESC;