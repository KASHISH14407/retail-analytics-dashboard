# ============================================================
# SALES ANALYSIS PROJECT - INTERMEDIATE LEVEL
# Tools: Python (Pandas, Matplotlib, Seaborn), SQL (SQLite)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import sqlite3
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# STEP 1: GENERATE SAMPLE DATASET
# ─────────────────────────────────────────────
np.random.seed(42)
n = 1000

regions     = ["North", "South", "East", "West"]
categories  = ["Electronics", "Clothing", "Furniture", "Food", "Sports"]
products    = {
    "Electronics": ["Laptop", "Phone", "Tablet", "Headphones"],
    "Clothing":    ["T-Shirt", "Jeans", "Jacket", "Dress"],
    "Furniture":   ["Chair", "Table", "Sofa", "Shelf"],
    "Food":        ["Snacks", "Beverages", "Dairy", "Bakery"],
    "Sports":      ["Shoes", "Gym Kit", "Cricket Bat", "Football"],
}

records = []
for i in range(1, n + 1):
    cat  = np.random.choice(categories)
    prod = np.random.choice(products[cat])
    qty  = np.random.randint(1, 20)
    price= round(np.random.uniform(10, 500), 2)
    disc = round(np.random.uniform(0, 0.3), 2)
    records.append({
        "order_id":    f"ORD{i:04d}",
        "date":        pd.Timestamp("2023-01-01") + pd.to_timedelta(np.random.randint(0, 365), unit="D"),
        "region":      np.random.choice(regions),
        "category":    cat,
        "product":     prod,
        "quantity":    qty,
        "unit_price":  price,
        "discount":    disc,
        "sales_rep":   f"Rep_{np.random.randint(1, 11)}",
    })

df = pd.DataFrame(records)
df["revenue"]      = round(df["quantity"] * df["unit_price"] * (1 - df["discount"]), 2)
df["profit"]       = round(df["revenue"] * np.random.uniform(0.1, 0.4, n), 2)
df["month"]        = df["date"].dt.month_name()
df["month_num"]    = df["date"].dt.month
df["quarter"]      = df["date"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})

print("✅ Dataset created:", df.shape)
print(df.head(3).to_string())

# ─────────────────────────────────────────────
# STEP 2: DATA CLEANING
# ─────────────────────────────────────────────
print("\n── Missing values ──")
print(df.isnull().sum())
print("\n── Duplicates:", df.duplicated().sum(), "──")
df.drop_duplicates(inplace=True)

print("\n── Basic Stats ──")
print(df[["revenue","profit","quantity","discount"]].describe().round(2))

# ─────────────────────────────────────────────
# STEP 3: SQL ANALYSIS (SQLite)
# ─────────────────────────────────────────────
conn = sqlite3.connect(":memory:")
df.to_sql("sales", conn, index=False, if_exists="replace")

queries = {
    "Revenue by Region": """
        SELECT region,
               ROUND(SUM(revenue),2)  AS total_revenue,
               ROUND(SUM(profit),2)   AS total_profit,
               COUNT(order_id)        AS total_orders
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """,
    "Top 5 Products": """
        SELECT product, category,
               ROUND(SUM(revenue),2) AS revenue,
               SUM(quantity)         AS units_sold
        FROM sales
        GROUP BY product, category
        ORDER BY revenue DESC
        LIMIT 5
    """,
    "Monthly Revenue Trend": """
        SELECT month_num, month,
               ROUND(SUM(revenue),2) AS revenue
        FROM sales
        GROUP BY month_num, month
        ORDER BY month_num
    """,
    "Category Performance": """
        SELECT category,
               ROUND(SUM(revenue),2)        AS revenue,
               ROUND(AVG(discount)*100,1)   AS avg_discount_pct,
               ROUND(SUM(profit)/SUM(revenue)*100,1) AS profit_margin_pct
        FROM sales
        GROUP BY category
        ORDER BY revenue DESC
    """,
    "Top 3 Sales Reps": """
        SELECT sales_rep,
               ROUND(SUM(revenue),2) AS revenue,
               COUNT(order_id)       AS orders
        FROM sales
        GROUP BY sales_rep
        ORDER BY revenue DESC
        LIMIT 3
    """,
}

results = {}
print("\n" + "="*55)
for title, q in queries.items():
    res = pd.read_sql_query(q, conn)
    results[title] = res
    print(f"\n📊 {title}")
    print(res.to_string(index=False))
    print("─"*55)

conn.close()

# ─────────────────────────────────────────────
# STEP 4: VISUALIZATIONS
# ─────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
fig, axes = plt.subplots(3, 2, figsize=(16, 18))
fig.suptitle("Sales Analysis Dashboard — 2023", fontsize=20, fontweight="bold", y=1.01)

# 1. Revenue by Region (bar)
ax = axes[0, 0]
reg = results["Revenue by Region"]
bars = ax.bar(reg["region"], reg["total_revenue"], color=sns.color_palette("Set2"))
ax.set_title("Revenue by Region", fontweight="bold")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+500,
            f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=9)

# 2. Monthly Revenue Trend (line)
ax = axes[0, 1]
monthly = results["Monthly Revenue Trend"]
ax.plot(monthly["month_num"], monthly["revenue"], marker="o", linewidth=2.5,
        color="#2ecc71", markersize=7)
ax.fill_between(monthly["month_num"], monthly["revenue"], alpha=0.15, color="#2ecc71")
ax.set_title("Monthly Revenue Trend", fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.set_xticks(monthly["month_num"])
ax.set_xticklabels([m[:3] for m in monthly["month"]], rotation=45)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# 3. Category Revenue (horizontal bar)
ax = axes[1, 0]
cat_data = results["Category Performance"].sort_values("revenue")
colors = sns.color_palette("coolwarm", len(cat_data))
ax.barh(cat_data["category"], cat_data["revenue"], color=colors)
ax.set_title("Revenue by Category", fontweight="bold")
ax.set_xlabel("Revenue ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# 4. Profit Margin by Category (bar)
ax = axes[1, 1]
ax.bar(cat_data["category"], cat_data["profit_margin_pct"],
       color=sns.color_palette("viridis", len(cat_data)))
ax.set_title("Profit Margin % by Category", fontweight="bold")
ax.set_ylabel("Profit Margin (%)")
ax.set_ylim(0, 35)
for i, v in enumerate(cat_data["profit_margin_pct"]):
    ax.text(i, v + 0.5, f"{v}%", ha="center", fontsize=9)

# 5. Revenue by Quarter (pie)
ax = axes[2, 0]
q_data = df.groupby("quarter")["revenue"].sum().reset_index().sort_values("quarter")
ax.pie(q_data["revenue"], labels=q_data["quarter"], autopct="%1.1f%%",
       colors=sns.color_palette("pastel"), startangle=90,
       wedgeprops={"edgecolor":"white","linewidth":1.5})
ax.set_title("Revenue Share by Quarter", fontweight="bold")

# 6. Top 5 Products (bar)
ax = axes[2, 1]
top5 = results["Top 5 Products"]
colors6 = sns.color_palette("tab10", len(top5))
ax.bar(top5["product"], top5["revenue"], color=colors6)
ax.set_title("Top 5 Products by Revenue", fontweight="bold")
ax.set_ylabel("Revenue ($)")
ax.set_xticklabels(top5["product"], rotation=20, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/sales_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Dashboard saved → sales_dashboard.png")

# ─────────────────────────────────────────────
# STEP 5: EXPORT TO EXCEL (for Power BI)
# ─────────────────────────────────────────────
excel_path = "/mnt/user-data/outputs/sales_data.xlsx"
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Raw Data", index=False)
    results["Revenue by Region"].to_excel(writer, sheet_name="Region Summary", index=False)
    results["Category Performance"].to_excel(writer, sheet_name="Category Summary", index=False)
    results["Monthly Revenue Trend"].to_excel(writer, sheet_name="Monthly Trend", index=False)
    results["Top 5 Products"].to_excel(writer, sheet_name="Top Products", index=False)

print(f"✅ Excel file saved → {excel_path}")
print("\n🎯 Power BI Steps:")
print("   1. Open Power BI Desktop")
print("   2. Get Data → Excel → select sales_data.xlsx")
print("   3. Load all sheets")
print("   4. Create relationships between sheets on 'category' / 'region'")
print("   5. Build visuals: Bar chart (region), Line chart (monthly), Pie (quarter)")

# ─────────────────────────────────────────────
# STEP 6: KEY BUSINESS INSIGHTS
# ─────────────────────────────────────────────
print("\n" + "="*55)
print("💡 KEY BUSINESS INSIGHTS")
print("="*55)
top_region   = results["Revenue by Region"].iloc[0]
top_product  = results["Top 5 Products"].iloc[0]
top_cat      = results["Category Performance"].iloc[0]
total_rev    = df["revenue"].sum()
total_profit = df["profit"].sum()

print(f"  Total Revenue   : ${total_rev:,.2f}")
print(f"  Total Profit    : ${total_profit:,.2f}")
print(f"  Overall Margin  : {total_profit/total_rev*100:.1f}%")
print(f"  Best Region     : {top_region['region']} (${top_region['total_revenue']:,.2f})")
print(f"  Best Product    : {top_product['product']} (${top_product['revenue']:,.2f})")
print(f"  Best Category   : {top_cat['category']} (${top_cat['revenue']:,.2f})")
print("="*55)
print("✅ Project Complete!")
