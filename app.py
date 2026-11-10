import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Page Settings
st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide"
)

# Load Data from SQLite
@st.cache_data
def load_data():
    conn = sqlite3.connect("retail_sales.db")
    df = pd.read_sql("SELECT * FROM sales", conn)
    conn.close()
    return df

data = load_data()

# Calculate Revenue
data["Revenue"] = data["Quantity"] * data["Price"]

# Dashboard Title
st.title("Retail Sales Analytics Dashboard")
st.success("Connected to SQLite Database!")

# Sidebar Filter
st.sidebar.header("Sales Filters")

regions = ["All"] + sorted(data["Region"].unique().tolist())

selected_region = st.sidebar.selectbox(
    "Select Region", regions
)

if selected_region != "All":
    filtered_data = data[data["Region"] == selected_region]
else:
    filtered_data = data

# KPI Metrics
total_revenue = filtered_data["Revenue"].sum()
total_orders = filtered_data["Order_ID"].count()
average_order = filtered_data["Revenue"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Average Order Value", f"₹{average_order:,.0f}")

# Product-wise Sales
st.subheader("1. Product-wise Sales")

product_sales = filtered_data.groupby("Product")["Quantity"].sum()
st.bar_chart(product_sales)

# Region-wise Revenue
st.subheader("2. Region-wise Revenue")

region_sales = filtered_data.groupby("Region")["Revenue"].sum()
st.bar_chart(region_sales)

# Product Revenue Pie Chart
st.subheader("3. Product Revenue Distribution")

product_revenue = filtered_data.groupby("Product")["Revenue"].sum()

fig, ax = plt.subplots()
ax.pie(
    product_revenue,
    labels=product_revenue.index,
    autopct="%1.1f%%"
)
st.pyplot(fig)
plt.close(fig)

# Sales Data Table
st.subheader("4. Sales Data")
st.dataframe(filtered_data)

# Download Report
st.subheader("5. Download Report")

csv_data = filtered_data.to_csv(index=False)

st.download_button(
    label="Download Sales Report",
    data=csv_data,
    file_name="sales_report.csv",
    mime="text/csv"
)

# Business Insights
st.subheader("6. Business Insights")

best_product = product_revenue.idxmax()
best_region = region_sales.idxmax()

st.write("Best Selling Product:", best_product)
st.write("Highest Revenue Region:", best_region)
st.write("Total Revenue Generated:", f"₹{total_revenue:,.0f}")
st.write("Total Units Sold:", filtered_data["Quantity"].sum())
# SQL Analysis
st.subheader("7. SQL Analysis")

conn = sqlite3.connect("retail_sales.db")

# 1. Product-wise Revenue
product_query = """
SELECT Product, SUM(Revenue) AS Total_Revenue
FROM sales
GROUP BY Product
ORDER BY Total_Revenue DESC
"""

sql_products = pd.read_sql_query(product_query, conn)

st.write("Product-wise Revenue Report")
st.dataframe(sql_products)

# 2. Region-wise Revenue
region_query = """
SELECT Region, SUM(Quantity * Price) AS Total_Revenue
FROM sales
GROUP BY Region
ORDER BY Total_Revenue DESC
"""

sql_regions = pd.read_sql_query(region_query, conn)

st.write("Region-wise Revenue Report")
st.dataframe(sql_regions)

# 3. Overall Sales Summary
summary_query = """
SELECT
    SUM(Quantity * Price) AS Total_Revenue,
    COUNT(Order_ID) AS Total_Orders,
    SUM(Quantity) AS Total_Quantity
FROM sales
"""

sql_summary = pd.read_sql_query(summary_query, conn)

st.write("Overall SQL Sales Summary")
st.dataframe(sql_summary)

conn.close()
