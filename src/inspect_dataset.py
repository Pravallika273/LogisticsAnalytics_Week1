import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# 1. File paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "raw" / "DataCoSupplyChainDataset.csv"

# ---------------------------------------------------------
# 2. Load dataset
# ---------------------------------------------------------

print("=" * 70)
print("DATACO SUPPLY CHAIN DATASET INSPECTION")
print("=" * 70)

df = pd.read_csv(
    DATA_FILE,
    encoding="latin-1",
    low_memory=False
)

# ---------------------------------------------------------
# 3. Basic information
# ---------------------------------------------------------

print("\n1. DATASET SHAPE")
print("-" * 70)
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]:,}")

print("\n2. COLUMN NAMES")
print("-" * 70)

for i, column in enumerate(df.columns, start=1):
    print(f"{i:2}. {column}")

# ---------------------------------------------------------
# 4. Data types
# ---------------------------------------------------------

print("\n3. DATA TYPES")
print("-" * 70)
print(df.dtypes.to_string())

# ---------------------------------------------------------
# 5. Missing values
# ---------------------------------------------------------

print("\n4. MISSING VALUES")
print("-" * 70)

missing = df.isnull().sum()

missing_report = pd.DataFrame({
    "Column": missing.index,
    "Missing_Count": missing.values,
    "Missing_Percentage": (missing.values / len(df) * 100).round(2)
})

missing_report = missing_report[
    missing_report["Missing_Count"] > 0
].sort_values(
    by="Missing_Count",
    ascending=False
)

if missing_report.empty:
    print("No missing values found.")
else:
    print(missing_report.to_string(index=False))

# ---------------------------------------------------------
# 6. Duplicate records
# ---------------------------------------------------------

print("\n5. DUPLICATE RECORDS")
print("-" * 70)

duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates:,}")

# ---------------------------------------------------------
# 7. First five rows
# ---------------------------------------------------------

print("\n6. FIRST FIVE ROWS")
print("-" * 70)
print(df.head().to_string())

# ---------------------------------------------------------
# 8. Important logistics variables
# ---------------------------------------------------------

important_columns = [
    "Order Id",
    "Order Status",
    "Shipping Mode",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Delivery Status",
    "Late_delivery_risk",
    "Market",
    "Order Region",
    "Order Country",
    "Category Name",
    "Customer Segment",
    "Order Item Quantity",
    "Order Item Total",
    "Order Profit Per Order"
]

print("\n7. IMPORTANT LOGISTICS COLUMNS")
print("-" * 70)

for column in important_columns:
    if column in df.columns:
        print(f"✓ {column}")
    else:
        print(f"✗ {column}  <-- NOT FOUND")

# ---------------------------------------------------------
# 9. Unique values for key categorical fields
# ---------------------------------------------------------

categorical_columns = [
    "Shipping Mode",
    "Delivery Status",
    "Market",
    "Customer Segment"
]

print("\n8. KEY CATEGORY VALUES")
print("-" * 70)

for column in categorical_columns:
    if column in df.columns:
        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False).to_string())

# ---------------------------------------------------------
# 10. Summary statistics for important numeric columns
# ---------------------------------------------------------

numeric_columns = [
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Late_delivery_risk",
    "Order Item Quantity",
    "Order Item Total",
    "Order Profit Per Order"
]

print("\n9. NUMERIC SUMMARY")
print("-" * 70)

available_numeric = [
    col for col in numeric_columns
    if col in df.columns
]

if available_numeric:
    print(df[available_numeric].describe().round(2).to_string())

# ---------------------------------------------------------
# 11. Save inspection report
# ---------------------------------------------------------

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

missing_report.to_csv(
    OUTPUT_DIR / "missing_value_report.csv",
    index=False
)

print("\n10. OUTPUT")
print("-" * 70)
print(
    f"Missing-value report saved to:\n"
    f"{OUTPUT_DIR / 'missing_value_report.csv'}"
)

print("\nDataset inspection completed successfully.")
print("=" * 70)