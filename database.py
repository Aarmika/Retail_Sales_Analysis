import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("retail_sales.db")

# Read CSV file
data = pd.read_csv("sales.csv")

# Calculate Revenue
data["Revenue"] = data["Quantity"] * data["Price"]

# Store data in SQLite
data.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

print("Data successfully stored in database!")

# Read data from database
result = pd.read_sql(
    "SELECT * FROM sales",
    conn
)

print(result)
query = """
SELECT Product, SUM(Revenue) AS Total_Revenue
FROM sales
GROUP BY Product
ORDER BY Total_Revenue DESC
"""

report = pd.read_sql(query, conn)

print("\nProduct Revenue Report:")
print(report)
conn.close()