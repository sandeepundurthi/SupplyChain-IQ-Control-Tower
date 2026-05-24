import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "sql" / "supply_chain.db"

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    warehouse_name,
    warehouse_region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(100.0 * AVG(is_delayed), 2) AS delay_rate,
    ROUND(AVG(delay_days), 2) AS avg_delay_days
FROM supply_chain_master
GROUP BY warehouse_name, warehouse_region
ORDER BY delay_rate DESC
LIMIT 10;
"""

df = pd.read_sql_query(query, conn)
print(df)

conn.close()
