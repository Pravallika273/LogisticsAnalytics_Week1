import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PATHS
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
# LOAD DATA
# ============================================================

df = pd.read_csv(DATA_FILE)


# ============================================================
# CHART 1
# DELIVERY STATUS
# ============================================================

status = (
    df["Delivery Status"]
    .value_counts()
)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    status.index,
    status.values
)

plt.title(
    "Delivery Status Distribution",
    fontsize=16,
    fontweight="bold"
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

for bar, value in zip(bars, status.values):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:,}",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.tight_layout()

plt.savefig(
    CHART_DIR / "REPORT_01_delivery_status.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# CHART 2
# SHIPPING MODE DELAY RATE
# ============================================================

shipping_mode = (
    df.groupby("Shipping Mode")["Is Delayed"]
    .mean()
    .sort_values(ascending=False)
    * 100
)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    shipping_mode.index,
    shipping_mode.values
)

plt.title(
    "Observed Late Delivery Rate by Shipping Mode",
    fontsize=16,
    fontweight="bold"
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

for bar, value in zip(
    bars,
    shipping_mode.values
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.ylim(
    0,
    max(shipping_mode.values) + 10
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "REPORT_02_shipping_mode_delay.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# CHART 3
# MARKET DELAY RATE
# ============================================================

market = (
    df.groupby("Market")["Is Delayed"]
    .mean()
    .sort_values(ascending=False)
    * 100
)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    market.index,
    market.values
)

plt.title(
    "Observed Late Delivery Rate by Market",
    fontsize=16,
    fontweight="bold"
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

for bar, value in zip(
    bars,
    market.values
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.1f}%",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.ylim(
    0,
    max(market.values) + 10
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "REPORT_03_market_delay.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# COMPLETION
# ============================================================

print("=" * 70)
print("REPORT CHARTS CREATED SUCCESSFULLY")
print("=" * 70)

print("\nCreated:")

print(
    CHART_DIR
    / "REPORT_01_delivery_status.png"
)

print(
    CHART_DIR
    / "REPORT_02_shipping_mode_delay.png"
)

print(
    CHART_DIR
    / "REPORT_03_market_delay.png"
)