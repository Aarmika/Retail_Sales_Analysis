
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

# Page Settings
st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide"
)

# Database and CSV paths
DB_PATH = Path("retail_sales.db")
CSV_PATH = Path("sales.csv")


# Load Data and Create SQLite Table if Missing
@st.cache_data
def load_data():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            "sales.csv not found. Please upload sales.csv to GitHub."
        )

    conn = sqlite3.connect(DB_PATH)

    try:
        # Check whether sales table exists
        table_check = pd.read_sql_query(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='sales'",
            conn
        )

        # Create table if it does not exist
        if table_check.empty:
            df = pd.read_csv(CSV_PATH)
            df["Revenue"] = df["Quantity"] * df["Price"]

            df.to_sql(
                "sales",
                conn,
                if_exists="replace",
                index=False
            )

        # Read data from SQLite
        data = pd.read_sql_query(
            "SELECT * FROM sales",
            conn
        )

    finally:
        conn.close()

    return data


# Load Data
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
    "Select Region",
    regions
)

if selected_region != "All":
    filtered_data = data[data["Region"] == selected_region]
else:
    filtered_data = data


# KPI Metrics
total_revenue = filtered_data["Revenue"].sum()
total_orders = filtered_data["Order_ID"].count()
average_order = (
    filtered_data["Revenue"].mean()
    if not filtered_data.empty else 0
)

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

if not product_revenue.empty:
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

if not product_revenue.empty:
    best_product = product_revenue.idxmax()
    best_region = region_sales.idxmax()

    st.write("Best Selling Product:", best_product)
    st.write("Highest Revenue Region:", best_region)

st.write("Total Revenue Generated:", f"₹{total_revenue:,.0f}")
st.write("Total Units Sold:", filtered_data["Quantity"].sum())


# SQL Analysis
st.subheader("7. SQL Analysis")

conn = sqlite3.connect(DB_PATH)

try:
    # Product-wise Revenue
    product_query = """
    SELECT Product, SUM(Revenue) AS Total_Revenue
    FROM sales
    GROUP BY Product
    ORDER BY Total_Revenue DESC
    """

    sql_products = pd.read_sql_query(product_query, conn)

    st.write("Product-wise Revenue Report")
    st.dataframe(sql_products)


    # Region-wise Revenue
    region_query = """
    SELECT Region, SUM(Quantity * Price) AS Total_Revenue
    FROM sales
    GROUP BY Region
    ORDER BY Total_Revenue DESC
    """

    sql_regions = pd.read_sql_query(region_query, conn)

    st.write("Region-wise Revenue Report")
    st.dataframe(sql_regions)


    # Overall Sales Summary
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

finally:
    conn.close()
