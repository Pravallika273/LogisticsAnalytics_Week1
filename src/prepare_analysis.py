import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "DataCoSupplyChainDataset.csv"
)

PROCESSED_DIR = BASE_DIR / "data" / "processed"
CHART_DIR = BASE_DIR / "outputs" / "charts"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 75)
print("LOGISTICS ANALYTICS - DATA PREPARATION")
print("=" * 75)

df = pd.read_csv(
    DATA_FILE,
    encoding="latin-1",
    low_memory=False
)

print(f"\nOriginal dataset shape: {df.shape}")


# ============================================================
# 3. REMOVE UNUSED / HIGH-MISSING COLUMNS
# ============================================================

# Product Description is 100% missing.
# Order Zipcode has very high missingness and is not required
# for our Week 1 logistics analysis.

columns_to_remove = [
    "Product Description",
    "Order Zipcode"
]

existing_columns = [
    col for col in columns_to_remove
    if col in df.columns
]

df = df.drop(columns=existing_columns)

print("\nRemoved columns:")
for column in existing_columns:
    print(f"  - {column}")


# ============================================================
# 4. HANDLE SMALL AMOUNTS OF MISSING DATA
# ============================================================

# Customer Lname has only 8 missing values.
# Customer Zipcode has only 3 missing values.
# These fields are not needed for our logistics KPIs,
# so we will not use them in the analysis.

print("\nRemaining missing values in important analysis columns:")

analysis_columns = [
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Delivery Status",
    "Late_delivery_risk",
    "Shipping Mode",
    "Market",
    "Order Region",
    "Order Country",
    "Customer Segment",
    "Order Item Quantity",
    "Order Item Total",
    "Order Profit Per Order"
]

for column in analysis_columns:
    if column in df.columns:
        missing = df[column].isna().sum()
        print(f"  {column}: {missing:,}")


# ============================================================
# 5. DATE CONVERSION
# ============================================================

df["order date (DateOrders)"] = pd.to_datetime(
    df["order date (DateOrders)"],
    errors="coerce"
)

df["shipping date (DateOrders)"] = pd.to_datetime(
    df["shipping date (DateOrders)"],
    errors="coerce"
)


# ============================================================
# 6. FEATURE ENGINEERING
# ============================================================

# Difference between actual and scheduled shipping time

df["Shipping Delay Days"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

# Positive value = slower than scheduled
# Zero = exactly on schedule
# Negative value = faster than scheduled


# Delivery delay flag based on Delivery Status

df["Is Delayed"] = (
    df["Delivery Status"] == "Late delivery"
).astype(int)


# On-time / successful shipping flag

df["Is On Time"] = (
    df["Delivery Status"] == "Shipping on time"
).astype(int)


# Advance shipping flag

df["Is Advance"] = (
    df["Delivery Status"] == "Advance shipping"
).astype(int)


# ============================================================
# 7. KPI CALCULATIONS
# ============================================================

total_records = len(df)

late_orders = df["Is Delayed"].sum()

on_time_orders = df["Is On Time"].sum()

advance_orders = df["Is Advance"].sum()

cancelled_orders = (
    df["Delivery Status"] == "Shipping canceled"
).sum()


delivery_delay_rate = (
    late_orders / total_records
) * 100


on_time_rate = (
    on_time_orders / total_records
) * 100


average_actual_shipping_time = (
    df["Days for shipping (real)"].mean()
)


average_scheduled_shipping_time = (
    df["Days for shipment (scheduled)"].mean()
)


average_shipping_delay = (
    df["Shipping Delay Days"].mean()
)


average_order_value = (
    df["Order Item Total"].mean()
)


# ============================================================
# 8. DISPLAY KPI RESULTS
# ============================================================

print("\n")
print("=" * 75)
print("LOGISTICS KPI RESULTS")
print("=" * 75)

print(f"\nTotal records                  : {total_records:,}")

print(
    f"Late delivery records         : "
    f"{late_orders:,}"
)

print(
    f"On-time delivery records      : "
    f"{on_time_orders:,}"
)

print(
    f"Advance shipping records      : "
    f"{advance_orders:,}"
)

print(
    f"Cancelled shipping records    : "
    f"{cancelled_orders:,}"
)

print(
    f"\nDelivery delay rate            : "
    f"{delivery_delay_rate:.2f}%"
)

print(
    f"On-time shipping rate          : "
    f"{on_time_rate:.2f}%"
)

print(
    f"Average actual shipping time  : "
    f"{average_actual_shipping_time:.2f} days"
)

print(
    f"Average scheduled shipping    : "
    f"{average_scheduled_shipping_time:.2f} days"
)

print(
    f"Average shipping difference   : "
    f"{average_shipping_delay:.2f} days"
)

print(
    f"Average order value           : "
    f"${average_order_value:.2f}"
)


# ============================================================
# 9. SHIPPING MODE ANALYSIS
# ============================================================

shipping_mode_summary = (
    df.groupby("Shipping Mode")
    .agg(
        Orders=("Order Id", "count"),
        Average_Actual_Days=(
            "Days for shipping (real)",
            "mean"
        ),
        Average_Scheduled_Days=(
            "Days for shipment (scheduled)",
            "mean"
        ),
        Delay_Rate=("Is Delayed", "mean")
    )
    .reset_index()
)

shipping_mode_summary["Delay_Rate"] *= 100

shipping_mode_summary = shipping_mode_summary.round(2)


print("\n")
print("=" * 75)
print("SHIPPING MODE ANALYSIS")
print("=" * 75)

print(
    shipping_mode_summary.to_string(index=False)
)


# ============================================================
# 10. MARKET ANALYSIS
# ============================================================

market_summary = (
    df.groupby("Market")
    .agg(
        Orders=("Order Id", "count"),
        Average_Actual_Days=(
            "Days for shipping (real)",
            "mean"
        ),
        Delay_Rate=("Is Delayed", "mean"),
        Average_Order_Value=(
            "Order Item Total",
            "mean"
        )
    )
    .reset_index()
)

market_summary["Delay_Rate"] *= 100

market_summary = market_summary.round(2)


print("\n")
print("=" * 75)
print("MARKET ANALYSIS")
print("=" * 75)

print(
    market_summary.to_string(index=False)
)


# ============================================================
# 11. SAVE PROCESSED DATA
# ============================================================

processed_file = (
    PROCESSED_DIR
    / "logistics_analysis_ready.csv"
)

df.to_csv(
    processed_file,
    index=False
)

print("\nProcessed dataset saved to:")
print(processed_file)


# ============================================================
# 12. SAVE KPI TABLE
# ============================================================

kpi_table = pd.DataFrame({
    "KPI": [
        "Total Records",
        "Delivery Delay Rate",
        "On-Time Shipping Rate",
        "Average Actual Shipping Time",
        "Average Scheduled Shipping Time",
        "Average Shipping Difference",
        "Average Order Value"
    ],
    "Value": [
        total_records,
        round(delivery_delay_rate, 2),
        round(on_time_rate, 2),
        round(average_actual_shipping_time, 2),
        round(average_scheduled_shipping_time, 2),
        round(average_shipping_delay, 2),
        round(average_order_value, 2)
    ]
})

kpi_file = PROCESSED_DIR / "logistics_kpis.csv"

kpi_table.to_csv(
    kpi_file,
    index=False
)

print("\nKPI table saved to:")
print(kpi_file)


# ============================================================
# 13. CHART 1 — DELIVERY STATUS
# ============================================================

delivery_counts = (
    df["Delivery Status"]
    .value_counts()
)

plt.figure(figsize=(10, 6))

delivery_counts.plot(
    kind="bar"
)

plt.title(
    "Distribution of Delivery Status"
)

plt.xlabel(
    "Delivery Status"
)

plt.ylabel(
    "Number of Records"
)

plt.xticks(
    rotation=20,
    ha="right"
)

plt.tight_layout()

chart1 = (
    CHART_DIR
    / "delivery_status_distribution.png"
)

plt.savefig(
    chart1,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 14. CHART 2 — SHIPPING MODE
# ============================================================

shipping_counts = (
    df["Shipping Mode"]
    .value_counts()
)

plt.figure(figsize=(10, 6))

shipping_counts.plot(
    kind="bar"
)

plt.title(
    "Orders by Shipping Mode"
)

plt.xlabel(
    "Shipping Mode"
)

plt.ylabel(
    "Number of Records"
)

plt.xticks(
    rotation=20,
    ha="right"
)

plt.tight_layout()

chart2 = (
    CHART_DIR
    / "shipping_mode_distribution.png"
)

plt.savefig(
    chart2,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 15. CHART 3 — DELAY RATE BY MARKET
# ============================================================

market_delay = (
    df.groupby("Market")["Is Delayed"]
    .mean()
    .sort_values(ascending=False)
    * 100
)

plt.figure(figsize=(10, 6))

market_delay.plot(
    kind="bar"
)

plt.title(
    "Delivery Delay Rate by Market"
)

plt.xlabel(
    "Market"
)

plt.ylabel(
    "Delay Rate (%)"
)

plt.xticks(
    rotation=20,
    ha="right"
)

plt.tight_layout()

chart3 = (
    CHART_DIR
    / "delay_rate_by_market.png"
)

plt.savefig(
    chart3,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 16. COMPLETION MESSAGE
# ============================================================

print("\n")
print("=" * 75)
print("DATA PREPARATION AND KPI ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 75)

print("\nCreated files:")
print(f"1. {processed_file}")
print(f"2. {kpi_file}")
print(f"3. {chart1}")
print(f"4. {chart2}")
print(f"5. {chart3}")