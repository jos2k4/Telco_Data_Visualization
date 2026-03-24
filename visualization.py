import sqlite3 as lite
import pandas as pd
import matplotlib.pyplot as plt
# define database path
db_path = 'data.db'
conn = lite.connect(db_path)
cursor = conn.cursor()

#Visualisierung: Umsatz sortiert nach PLZ

df_revenue = pd.read_sql_query("""
    SELECT c.zip_code, SUM(p.Plan_price) AS Total_Revenue
    FROM customer c
    JOIN Contracts con ON c.customer_id = con.customer_id
    JOIN Plans p ON con.Plan_id = p.Plan_id
    GROUP BY c.zip_code
    ORDER BY Total_Revenue DESC;
""", conn)

plt.figure(figsize=(10, 6))
# casting zip code zum string
plt.bar(df_revenue['zip_code'].astype(str), df_revenue['Total_Revenue'], color='#E60000')
plt.title('Total Revenue by ZIP Code')
plt.xlabel('ZIP Code')
plt.ylabel('Revenue in €')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('revenue_chart.png') # Speichert das Bild
plt.show()

