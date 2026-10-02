import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "logistics_analysis_ready.csv"
)

CHART_DIR = (
    BASE_DIR
    / "outputs"
    / "charts"
)

CHART_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 75)
print("LOGISTICS ANALYTICS - EXPLORATORY ANALYSIS")
print("=" * 75)

df = pd.read_csv(DATA_FILE)

print(f"\nRecords loaded: {len(df):,}")


# ============================================================
# 3. SHIPPING MODE ANALYSIS
# ============================================================

shipping_mode = (
    df.groupby("Shipping Mode")
    .agg(
        Records=("Order Id", "count"),
        Average_Actual_Days=(
            "Days for shipping (real)",
            "mean"
        ),
        Average_Scheduled_Days=(
            "Days for shipment (scheduled)",
            "mean"
        ),
        Late_Delivery_Rate=(
            "Is Delayed",
            "mean"
        )
    )
    .reset_index()
)

shipping_mode["Late_Delivery_Rate"] *= 100

shipping_mode = shipping_mode.round(2)

print("\n")
print("=" * 75)
print("1. SHIPPING MODE PERFORMANCE")
print("=" * 75)

print(
    shipping_mode
    .sort_values(
        "Late_Delivery_Rate",
        ascending=False
    )
    .to_string(index=False)
)


# ============================================================
# 4. MARKET ANALYSIS
# ============================================================

market = (
    df.groupby("Market")
    .agg(
        Records=("Order Id", "count"),
        Average_Actual_Days=(
            "Days for shipping (real)",
            "mean"
        ),
        Average_Scheduled_Days=(
            "Days for shipment (scheduled)",
            "mean"
        ),
        Late_Delivery_Rate=(
            "Is Delayed",
            "mean"
        )
    )
    .reset_index()
)

market["Late_Delivery_Rate"] *= 100

market = market.round(2)

print("\n")
print("=" * 75)
print("2. MARKET PERFORMANCE")
print("=" * 75)

print(
    market
    .sort_values(
        "Late_Delivery_Rate",
        ascending=False
    )
    .to_string(index=False)
)


# ============================================================
# 5. CUSTOMER SEGMENT ANALYSIS
# ============================================================

customer_segment = (
    df.groupby("Customer Segment")
    .agg(
        Records=("Order Id", "count"),
        Average_Actual_Days=(
            "Days for shipping (real)",
            "mean"
        ),
        Late_Delivery_Rate=(
            "Is Delayed",
            "mean"
        ),
        Average_Order_Value=(
            "Order Item Total",
            "mean"
        )
    )
    .reset_index()
)

customer_segment["Late_Delivery_Rate"] *= 100

customer_segment = customer_segment.round(2)

print("\n")
print("=" * 75)
print("3. CUSTOMER SEGMENT PERFORMANCE")
print("=" * 75)

print(
    customer_segment
    .sort_values(
        "Late_Delivery_Rate",
        ascending=False
    )
    .to_string(index=False)
)


# ============================================================
# 6. ORDER REGION ANALYSIS
# ============================================================

region = (
    df.groupby("Order Region")
    .agg(
        Records=("Order Id", "count"),
        Average_Actual_Days=(
            "Days for shipping (real)",
            "mean"
        ),
        Late_Delivery_Rate=(
            "Is Delayed",
            "mean"
        )
    )
    .reset_index()
)

region["Late_Delivery_Rate"] *= 100

region = region.round(2)

print("\n")
print("=" * 75)
print("4. ORDER REGION PERFORMANCE")
print("=" * 75)

print(
    region
    .sort_values(
        "Late_Delivery_Rate",
        ascending=False
    )
    .to_string(index=False)
)


# ============================================================
# 7. SAVE ANALYSIS TABLES
# ============================================================

shipping_mode.to_csv(
    BASE_DIR
    / "data"
    / "processed"
    / "shipping_mode_analysis.csv",
    index=False
)

market.to_csv(
    BASE_DIR
    / "data"
    / "processed"
    / "market_analysis.csv",
    index=False
)

customer_segment.to_csv(
    BASE_DIR
    / "data"
    / "processed"
    / "customer_segment_analysis.csv",
    index=False
)

region.to_csv(
    BASE_DIR
    / "data"
    / "processed"
    / "region_analysis.csv",
    index=False
)


# ============================================================
# 8. CHART 1 — LATE DELIVERY RATE BY SHIPPING MODE
# ============================================================

plot_data = shipping_mode.sort_values(
    "Late_Delivery_Rate",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    plot_data["Shipping Mode"],
    plot_data["Late_Delivery_Rate"]
)

plt.title(
    "Late Delivery Rate by Shipping Mode"
)

plt.xlabel(
    "Shipping Mode"
)

plt.ylabel(
    "Late Delivery Rate (%)"
)

plt.xticks(
    rotation=20,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "late_delivery_by_shipping_mode.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 9. CHART 2 — LATE DELIVERY RATE BY MARKET
# ============================================================

plot_data = market.sort_values(
    "Late_Delivery_Rate",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    plot_data["Market"],
    plot_data["Late_Delivery_Rate"]
)

plt.title(
    "Late Delivery Rate by Market"
)

plt.xlabel(
    "Market"
)

plt.ylabel(
    "Late Delivery Rate (%)"
)

plt.xticks(
    rotation=20,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "late_delivery_by_market.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 10. CHART 3 — LATE DELIVERY RATE BY CUSTOMER SEGMENT
# ============================================================

plot_data = customer_segment.sort_values(
    "Late_Delivery_Rate",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    plot_data["Customer Segment"],
    plot_data["Late_Delivery_Rate"]
)

plt.title(
    "Late Delivery Rate by Customer Segment"
)

plt.xlabel(
    "Customer Segment"
)

plt.ylabel(
    "Late Delivery Rate (%)"
)

plt.xticks(
    rotation=20,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "late_delivery_by_customer_segment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 11. COMPLETION
# ============================================================

print("\n")
print("=" * 75)
print("EXPLORATORY ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 75)

print("\nAnalysis tables saved to:")
print(BASE_DIR / "data" / "processed")

print("\nCharts saved to:")
print(CHART_DIR)