import pandas as pd
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

OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. LOAD PROCESSED DATA
# ============================================================

print("=" * 75)
print("LOGISTICS ANALYTICS - KPI VALIDATION")
print("=" * 75)

df = pd.read_csv(DATA_FILE)

print(f"\nRecords loaded: {len(df):,}")


# ============================================================
# 3. BASIC COUNTS
# ============================================================

total_records = len(df)

late = (
    df["Delivery Status"] == "Late delivery"
).sum()

advance = (
    df["Delivery Status"] == "Advance shipping"
).sum()

on_time = (
    df["Delivery Status"] == "Shipping on time"
).sum()

cancelled = (
    df["Delivery Status"] == "Shipping canceled"
).sum()


# ============================================================
# 4. NON-CANCELLED RECORDS
# ============================================================

completed_shipments = (
    total_records - cancelled
)


# ============================================================
# 5. KPI 1 — LATE DELIVERY RATE
# ============================================================

late_delivery_rate = (
    late / total_records
) * 100


# ============================================================
# 6. KPI 2 — ON-SCHEDULE OR EARLY RATE
# ============================================================

on_schedule_or_early = (
    advance + on_time
)

on_schedule_or_early_rate = (
    on_schedule_or_early
    / completed_shipments
) * 100


# ============================================================
# 7. KPI 3 — AVERAGE ACTUAL SHIPPING TIME
# ============================================================

average_actual_days = (
    df["Days for shipping (real)"]
    .mean()
)


# ============================================================
# 8. KPI 4 — AVERAGE SCHEDULED SHIPPING TIME
# ============================================================

average_scheduled_days = (
    df["Days for shipment (scheduled)"]
    .mean()
)


# ============================================================
# 9. KPI 5 — SCHEDULE VARIANCE
# ============================================================

average_schedule_variance = (
    df["Shipping Delay Days"]
    .mean()
)


# ============================================================
# 10. KPI 6 — CANCELLATION RATE
# ============================================================

cancellation_rate = (
    cancelled / total_records
) * 100


# ============================================================
# 11. TRUE ORDER-LEVEL VALUE
# ============================================================

# Multiple rows can belong to the same order.
# Therefore, aggregate Order Item Total by Order Id.

order_level = (
    df.groupby("Order Id")
    .agg(
        Order_Value=("Order Item Total", "sum"),
        Total_Items=("Order Item Quantity", "sum")
    )
    .reset_index()
)

average_order_value = (
    order_level["Order_Value"].mean()
)


# ============================================================
# 12. DISPLAY RESULTS
# ============================================================

print("\n")
print("=" * 75)
print("VALIDATED LOGISTICS KPIs")
print("=" * 75)

print(
    f"\nTotal records                  : "
    f"{total_records:,}"
)

print(
    f"Completed/non-cancelled       : "
    f"{completed_shipments:,}"
)

print(
    f"Late deliveries               : "
    f"{late:,}"
)

print(
    f"Advance shipments             : "
    f"{advance:,}"
)

print(
    f"On-time shipments             : "
    f"{on_time:,}"
)

print(
    f"Cancelled shipments            : "
    f"{cancelled:,}"
)

print("\n--- KPI VALUES ---")

print(
    f"\n1. Late Delivery Rate         : "
    f"{late_delivery_rate:.2f}%"
)

print(
    f"2. On-Schedule/Early Rate     : "
    f"{on_schedule_or_early_rate:.2f}%"
)

print(
    f"3. Average Actual Shipping    : "
    f"{average_actual_days:.2f} days"
)

print(
    f"4. Average Scheduled Shipping : "
    f"{average_scheduled_days:.2f} days"
)

print(
    f"5. Average Schedule Variance  : "
    f"{average_schedule_variance:.2f} days"
)

print(
    f"6. Cancellation Rate           : "
    f"{cancellation_rate:.2f}%"
)

print(
    f"7. Average Order Value         : "
    f"${average_order_value:.2f}"
)


# ============================================================
# 13. CREATE KPI TABLE
# ============================================================

kpi_table = pd.DataFrame({
    "KPI": [
        "Late Delivery Rate",
        "On-Schedule/Early Rate",
        "Average Actual Shipping Time",
        "Average Scheduled Shipping Time",
        "Average Schedule Variance",
        "Cancellation Rate",
        "Average Order Value"
    ],

    "Value": [
        f"{late_delivery_rate:.2f}%",
        f"{on_schedule_or_early_rate:.2f}%",
        f"{average_actual_days:.2f} days",
        f"{average_scheduled_days:.2f} days",
        f"{average_schedule_variance:.2f} days",
        f"{cancellation_rate:.2f}%",
        f"${average_order_value:.2f}"
    ]
})


# ============================================================
# 14. SAVE KPI TABLE
# ============================================================

output_file = (
    OUTPUT_DIR
    / "validated_kpis.csv"
)

kpi_table.to_csv(
    output_file,
    index=False
)

print("\n")
print("=" * 75)
print("KPI TABLE SAVED")
print("=" * 75)

print(output_file)

print("\nKPI validation completed successfully.")