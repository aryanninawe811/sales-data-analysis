import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("sales.csv")
df["Revenue"] = df["Units_Sold"] * df["Unit_Price"]
print("SALES DATA ANALYSIS")
print("--------------------")
print("Total Units Sold:", df["Units_Sold"].sum())
print("Total Revenue: ₹", df["Revenue"].sum())
print("Average Sale Revenue: ₹", round(df["Revenue"].mean(), 2))
product_revenue = df.groupby("Product")["Revenue"].sum()

print("\nPRODUCT-WISE REVENUE")
print(product_revenue)

print("\nHighest Revenue Product:", product_revenue.idxmax())
region_revenue = df.groupby("Region")["Revenue"].sum()

print("\nREGION-WISE REVENUE")
print(region_revenue)

print("\nTop Revenue Region:", region_revenue.idxmax())
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

monthly_revenue = df.groupby("Month")["Revenue"].sum()

print("\nMONTH-WISE REVENUE")
print(monthly_revenue)
plt.figure(figsize=(10, 5))
product_revenue.sort_values().plot(kind="bar", color="skyblue")
plt.title("Product-wise Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("product_revenue.png")
plt.show()
plt.figure(figsize=(10, 5))
monthly_revenue.plot(kind="line", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.grid(True)
plt.tight_layout()
plt.savefig("monthly_revenue.png")
plt.show()
df.to_csv("sales_report.csv", index=False)

print("\nSales report saved as sales_report.csv")