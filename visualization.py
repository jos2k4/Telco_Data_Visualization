import sqlite3 as lite
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Name der Datei
db_path = 'data.db'
#stellt connection zur Datei her
conn = lite.connect(db_path)
#curser initialisieren
cursor = conn.cursor()

#Visualisierung: Umsatz sortiert nach PLZ

df_revenue = pd.read_sql_query("""
    SELECT c.zip_code, SUM(p.Plan_price) AS Total_Revenue       --summiert den Preis pro zip-code
    FROM customer c
    JOIN Contracts con ON c.customer_id = con.customer_id
    JOIN Plans p ON con.Plan_id = p.Plan_id
    GROUP BY c.zip_code
    ORDER BY Total_Revenue DESC;
""", conn)

plt.figure(figsize=(10, 6))
# casting zip code zum string, um Visualisierung zu ermöglichen -> Sonst (Zip-Code1 1 2 3... Zip-Code2)
plt.bar(df_revenue['zip_code'].astype(str), df_revenue['Total_Revenue'], color='red')
#                      x-Achse                      y-Achse                     rot

#Beschreibung
plt.title('Total Revenue by ZIP Code')
plt.xlabel('ZIP Code')
plt.ylabel('Revenue in €')
sns.set_style("whitegrid")
plt.savefig('revenue_chart.png')            # Speichert das Bild
#Schließen, um Speicher zu sparen
plt.close()


#Visualisierung: Kunde, der 60% oder weniger seines Volumens verbraucht gilt als High-Risk-Customer
df_risk = pd.read_sql_query("""SELECT
    c.name, c.surname, u.GB_consumed, p.data_limit_GB, p.Plan_name, p.Plan_price,
    (u.GB_consumed * 100.0 / p.data_limit_GB) AS usage_percentage       --wie viel % des Datenvolumen verbraucht wurde


FROM customer c
    JOIN Contracts con ON c.customer_id = con.customer_id
    JOIN Plans p ON con.Plan_id = p.Plan_id
    JOIN usage u ON con.Contract_id = u.Contract_id
WHERE u.GB_consumed < (p.data_limit_GB * 0.6)       -- wenn verbrauchtes Volumen weniger als 60% des Tarifes sind
    AND con.Status = 'Active'                       --Kunde muss aktiven Vertrag haben
ORDER BY p.Plan_price DESC;""", conn)

#Größe
plt.figure(figsize=(10, 6))

sns.barplot(data = df_risk, x = 'name', y = 'usage_percentage', hue = 'Plan_name')
#              datenquelle         x           y                 zeigt den Vertrag an

#Beschreibung
plt.title('High-Risk-Customers')
plt.xlabel('Customer Name')
plt.ylabel('Usage in %')
sns.set_style("whitegrid")
plt.savefig('risk_chart.png')
#schließen, um Speicher zu sparen
plt.close()

#Logik: Wenn 80% oder mehr des Datenvolumens verbraucht werden, dann wird ein Upgrade vorgeschlagen
df_upgrade = pd.read_sql_query("""SELECT
    c.name, c.surname, u.GB_consumed, p.data_limit_GB, p.Plan_name,
        (u.GB_consumed * 100.0 / p.data_limit_GB) AS usage_percentage       --wie viel % des Datenvolumen verbraucht wurde


FROM customer c
    JOIN Contracts con ON c.customer_id = con.customer_id
    JOIN Plans p ON con.Plan_id = p.Plan_id
    JOIN usage u ON con.Contract_id = u.Contract_id
WHERE u.GB_consumed > (p.data_limit_GB * 0.8)       --verbrauchtes Datenvolumen wird mit 80% des Limits verglichen
ORDER BY u.GB_consumed DESC;""", conn)


plt.figure(figsize=(10, 6))
sns.barplot(data = df_upgrade, x = 'name', y = 'usage_percentage', hue = 'Plan_name')
#               Datenquelle         x               y                   zeigt die Vertrags Namen

#Beschreibung
plt.title('Customers with Upgrade potential')
plt.xlabel('Customer Name')
plt.ylabel('Usage in %')
sns.set_style("whitegrid")
#Speicherng
plt.savefig('upgrade_chart.png')
#Schließen, um Speicher zu sparen
plt.close()