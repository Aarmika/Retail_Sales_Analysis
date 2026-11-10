import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("sales.csv")

print(data)
print(data.tail())
print(data.head())
print(data.shape)
print(data.columns)
print(data.info())
print(data.describe())
print(data.isnull().sum())
data["Revenue"] = data["Quantity"] * data["Price"]

print(data)
# 1. Total Revenue
total_revenue = data["Revenue"].sum()
print("Total Revenue:", total_revenue)

# 2. Product-wise Sales
product_sales = data.groupby("Product")["Quantity"].sum()
print("\nProduct-wise Sales:")
print(product_sales)

# 3. Best Selling Product
best_product = product_sales.idxmax()
print("\nBest Selling Product:", best_product)

# 4. Region-wise Revenue
region_sales = data.groupby("Region")["Revenue"].sum()
print("\nRegion-wise Revenue:")
print(region_sales)

# 5. Average Order Value
average_order = data["Revenue"].mean()
print("\nAverage Order Value:", average_order)

# 6. Total Orders
total_orders = data["Order_ID"].count()
print("\nTotal Orders:", total_orders)
# Product-wise Sales Graph
plt.figure(figsize=(8, 5))

product_sales.plot(kind="bar")

plt.title("Product-wise Sales")
plt.xlabel("Products")
plt.ylabel("Quantity Sold")

plt.tight_layout()
plt.savefig("product_sales.png")
plt.show()
# Region-wise Revenue Graph
plt.figure(figsize=(8, 5))

region_sales.plot(kind="bar")

plt.title("Region-wise Revenue")
plt.xlabel("Regions")
plt.ylabel("Revenue")

plt.tight_layout()
plt.savefig("region_sales.png")
plt.show()
# Product Distribution Pie Chart
plt.figure(figsize=(7, 7))

product_sales.plot(kind="pie", autopct="%1.1f%%")

plt.title("Product Sales Distribution")
plt.ylabel("")

plt.tight_layout()
plt.savefig("product_distribution.png")
plt.show()
# 1. Highest Revenue Product
product_revenue = data.groupby("Product")["Revenue"].sum()

highest_product = product_revenue.idxmax()
print("\nHighest Revenue Product:", highest_product)

# 2. Highest Revenue Region
region_revenue = data.groupby("Region")["Revenue"].sum()

highest_region = region_revenue.idxmax()
print("Highest Revenue Region:", highest_region)

# 3. Lowest Revenue Product
lowest_product = product_revenue.idxmin()
print("Lowest Revenue Product:", lowest_product)

# 4. Total Quantity Sold
total_quantity = data["Quantity"].sum()
print("Total Quantity Sold:", total_quantity)

# 5. Maximum Revenue Order
max_order = data.loc[data["Revenue"].idxmax()]

print("\nHighest Revenue Order:")
print(max_order)
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Retail Sales Dashboard",
                   layout="wide")

st.title("Retail Sales Analytics Dashboard")

data = pd.read_csv("sales.csv")

data["Revenue"] = data["Quantity"] * data["Price"]

total_revenue = data["Revenue"].sum()
total_orders = data["Order_ID"].count()
average_order = data["Revenue"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Average Order Value", f"₹{average_order:,.0f}")
