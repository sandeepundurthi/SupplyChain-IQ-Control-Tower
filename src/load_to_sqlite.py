import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_DIR = BASE_DIR / "sql"
DB_DIR.mkdir(parents=True, exist_ok=True)

db_path = DB_DIR / "supply_chain.db"

conn = sqlite3.connect(db_path)

files = {
    "supply_chain_master": "supply_chain_master.csv",
    "orders": "orders_clean.csv",
    "shipments": "shipments_clean.csv",
    "inventory": "inventory_clean.csv"
}

for table_name, file_name in files.items():
    df = pd.read_csv(PROCESSED_DIR / file_name)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {table_name}: {df.shape}")

conn.close()

print("SQLite database created successfully.")
print(f"Database saved at: {db_path}")
