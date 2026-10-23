import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sales.csv"
REQUIRED_COLUMNS = [
    "Date", "Product", "Category", "Region",
    "Units_Sold", "Unit_Price"
]


def load_sales_data():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("sales.csv was not found.")

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError("sales.csv contains no sales records.")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    df = df[REQUIRED_COLUMNS].copy()

    for col in ["Product", "Category", "Region"]:
        df[col] = df[col].astype("string").str.strip()
        if df[col].isna().any() or df[col].eq("").any():
            raise ValueError(f"{col} contains missing or empty values.")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if df["Date"].isna().any():
        raise ValueError("Date contains invalid or missing values.")

    for col in ["Units_Sold", "Unit_Price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().any():
            raise ValueError(f"{col} contains non-numeric or missing values.")
        if (df[col] < 0).any():
            raise ValueError(f"{col} cannot contain negative values.")

    if (df["Units_Sold"] % 1 != 0).any():
        raise ValueError("Units_Sold must contain whole numbers.")

    df["Units_Sold"] = df["Units_Sold"].astype(int)
    df["Revenue"] = df["Units_Sold"] * df["Unit_Price"]
    df["Month"] = df["Date"].dt.to_period("M")

    return df


def main():
    try:
        df = load_sales_data()
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        print(f"Could not analyze sales data: {error}")
        return

    print("\nSALES DATA ANALYSIS")
    print("-------------------")
    print("Total records:", len(df))
    print("Total units sold:", df["Units_Sold"].sum())
    print(f"Total revenue: ₹{df['Revenue'].sum():,.2f}")
    print(f"Average revenue per record: ₹{df['Revenue'].mean():,.2f}")

    product_revenue = df.groupby("Product")["Revenue"].sum().sort_values(
        ascending=False
    )
    region_revenue = df.groupby("Region")["Revenue"].sum().sort_values(
        ascending=False
    )
    monthly_revenue = df.groupby("Month")["Revenue"].sum()

    print("\nPRODUCT-WISE REVENUE")
    print(product_revenue)
    print("\nHighest-revenue product:", product_revenue.idxmax())

    print("\nREGION-WISE REVENUE")
    print(region_revenue)
    print("\nTop-revenue region:", region_revenue.idxmax())

    print("\nMONTH-WISE REVENUE")
    print(monthly_revenue)

    report_file = BASE_DIR / "sales_report.csv"
    df.to_csv(report_file, index=False)
    print(f"\nSales report saved to: {report_file.name}")

    product_chart = BASE_DIR / "product_revenue.png"
    plt.figure(figsize=(10, 5))
    product_revenue.sort_values().plot(kind="bar")
    plt.title("Product-wise Revenue")
    plt.xlabel("Product")
    plt.ylabel("Revenue (₹)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(product_chart)
    plt.close()

    monthly_chart = BASE_DIR / "monthly_revenue.png"
    plt.figure(figsize=(10, 5))
    monthly_revenue.plot(kind="line", marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue (₹)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(monthly_chart)
    plt.close()

    print("Charts saved successfully.")
    print("Sales analysis completed!")


if __name__ == "__main__":
    main()
