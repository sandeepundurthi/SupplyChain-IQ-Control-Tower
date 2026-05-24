import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from sklearn.ensemble import RandomForestClassifier
import joblib

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    BASE_DIR / "data" / "processed" / "supply_chain_master.csv"
)

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv(DATA_PATH)

# -----------------------------
# Select Features
# -----------------------------
features = [
    "warehouse_region",
    "product_category",
    "customer_region",
    "customer_segment",
    "order_priority",
    "quantity",
    "sales_amount",
    "shipping_cost",
    "supplier_reliability_score"
]

target = "is_delayed"

df_model = df[features + [target]].copy()

# -----------------------------
# Encode categorical columns
# -----------------------------
label_encoders = {}

categorical_cols = [
    "warehouse_region",
    "product_category",
    "customer_region",
    "customer_segment",
    "order_priority"
]

for col in categorical_cols:
    le = LabelEncoder()
    df_model[col] = le.fit_transform(df_model[col])
    label_encoders[col] = le

# -----------------------------
# Split Data
# -----------------------------
X = df_model[features]
y = df_model[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# Train Model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -----------------------------
# Predictions
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print(round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -----------------------------
# Feature Importance
# -----------------------------
importance_df = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance_df)

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(model, MODEL_DIR / "delay_prediction_model.pkl")

joblib.dump(
    label_encoders,
    MODEL_DIR / "label_encoders.pkl"
)

print("\nModel saved successfully.")
