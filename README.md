# 📊 Retail Analytics Dashboard

> Analyzes 1,000 sales transactions across 4 regions, 5 categories & 10 sales reps using Python and SQL. Outputs a 6-panel Matplotlib dashboard and a Power BI-ready Excel file with multi-sheet summaries.

![Sales Dashboard](sales_dashboard.png)

---

## 🎯 Project Overview

A complete end-to-end sales data analysis project built entirely in Python. This project simulates a real-world business intelligence workflow — starting from raw data generation, moving through data cleaning and SQL-based analysis, and finishing with a fully visualized multi-panel dashboard and a Power BI-ready Excel export.

The dataset covers a full fiscal year (2023) with:
- **1,000** sales orders
- **4 regions** — North, South, East, West
- **5 product categories** — Electronics, Clothing, Furniture, Food, Sports
- **16 unique products** across all categories
- **10 sales representatives**
- **12 months** of transactions with realistic pricing and discounts

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `Python 3.x` | Core programming language |
| `Pandas` | Data manipulation and analysis |
| `NumPy` | Numerical operations and data generation |
| `Matplotlib` | Base plotting and dashboard layout |
| `Seaborn` | Chart styling and color palettes |
| `SQLite3` | In-memory relational database |
| `SQL` | Data querying and aggregation |
| `OpenPyXL` | Excel file generation |

---

## 🔄 Project Workflow

### Step 1 — Data Generation
Simulates 1,000 realistic sales records using NumPy. Each record includes order ID, date, region, category, product, quantity, unit price, discount, and sales rep. Revenue, profit, month, and quarter are calculated automatically.

### Step 2 — Data Cleaning
- Checks for missing values and duplicates
- Generates descriptive statistics across all numerical columns
- Ensures data is analysis-ready before querying

### Step 3 — SQL Analysis with SQLite
Runs 5 targeted SQL queries:
- **Revenue by Region** — total revenue, profit, and order count per region
- **Top 5 Products** — highest-earning products by revenue and units sold
- **Monthly Revenue Trend** — month-by-month revenue breakdown
- **Category Performance** — revenue, average discount, and profit margin per category
- **Top 3 Sales Reps** — best-performing reps by revenue and order volume

### Step 4 — Data Visualization
Builds a **6-panel dashboard** using Matplotlib and Seaborn:
1. Revenue by Region — bar chart with value annotations
2. Monthly Revenue Trend — line chart with area fill
3. Revenue by Category — horizontal bar chart
4. Profit Margin % by Category — bar chart
5. Revenue Share by Quarter — pie chart
6. Top 5 Products by Revenue — bar chart

### Step 5 — Excel Export
Exports all results into a structured multi-sheet Excel workbook:
- Sheet 1 — Raw Data
- Sheet 2 — Region Summary
- Sheet 3 — Category Summary
- Sheet 4 — Monthly Trend
- Sheet 5 — Top Products

### Step 6 — Business Insights
Automatically prints key metrics — total revenue, total profit, overall margin, best region, top product, and best category.

---

## 📈 Key Business Insights

| Metric | Value |
|--------|-------|
| 💰 Total Revenue | $2,117,559 |
| 📦 Total Orders | 1,000 |
| 🏆 Best Region | North — $568,706 |
| 🥇 Top Product | Table — $133,000 |
| 📊 Best Category | Clothing |
| 📅 Peak Months | March & August |
| 💹 Highest Margin | Food — 25.3% |
| 📉 Weakest Quarter | Q2 — 24.0% share |

---

## 📁 Repository Structure

```
retail-analytics-dashboard/
│
├── sales_analysis.py        ← Main analysis script
├── sales_data.xlsx          ← Generated Excel export (5 sheets)
├── sales_dashboard.png      ← Exported dashboard image
├── requirements.txt         ← Python dependencies
└── README.md                ← Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
Python 3.7 or higher installed on your machine.

### Installation

```bash
# Clone the repository
git clone https://github.com/KASHISH14407/retail-analytics-dashboard.git

# Navigate into the project folder
cd retail-analytics-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the analysis
python sales_analysis.py
```

### Requirements
```
pandas
numpy
matplotlib
seaborn
openpyxl
```

---

## 🔌 Power BI Integration

The exported `sales_data.xlsx` is structured for direct import into Power BI:

1. Open **Power BI Desktop**
2. Click **Get Data → Excel**
3. Select `sales_data.xlsx` and load all 5 sheets
4. Create relationships between sheets on `category` and `region` fields
5. Build visuals — bar chart for regions, line chart for monthly trend, pie for quarters


## 📄 License

This project is licensed under the MIT License — feel free to use, modify, and distribute it.

---

## 👤 Author

**Kashish**
- GitHub: [@KASHISH14407](https://github.com/KASHISH14407)

---

> *"Without data you're just another person with an opinion."* — W. Edwards Deming
