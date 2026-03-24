import sqlite3 as lite
import pandas as pd
import matplotlib.pyplot as plt
# define database path
db_path = 'data.db'
conn = lite.connect(db_path)
cursor = conn.cursor()

print("\n--- Auswertung abgeschlossen ---")
print("Data for visualization")

#Logik: PLZ mit jeweiligen Umsatz wird sortiert aufgelistet
cursor.execute("""SELECT c.zip_code, SUM(p.Plan_price) AS Total_Revenue
    FROM customer c
        JOIN Contracts con ON c.customer_id = con.customer_id
        JOIN Plans p ON con.Plan_id = p.Plan_id
    GROUP BY c.zip_code
ORDER BY p.Plan_price DESC;""")
rows = cursor.fetchall()

for row in rows:
    print(row)

#average revenue per user
print("ARPU:")

#Logik: ARPU = Gesamterlös / Anzahl Aktiver Kunden
cursor.execute("""SELECT AVG(p.Plan_price) AS ARPU
    FROM Contracts con
        JOIN Plans p ON con.Plan_id = p.Plan_id
WHERE con.Status = 'Active';""")

rows = cursor.fetchall()
for row in rows:
    print(row)


#clients with upgrade potential
print("Clients with upgrade potential")

#Logik: Wenn 90% oder mehr des Datenvolumens verbraucht werden, dann wird ein Upgrade vorgeschlagen
cursor.execute("""SELECT
    c.name, c.surname, u.GB_consumed, p.data_limit_GB, p.Plan_name

FROM customer c
    JOIN Contracts con ON c.customer_id = con.customer_id
    JOIN Plans p ON con.Plan_id = p.Plan_id
    JOIN usage u ON con.Contract_id = u.Contract_id
WHERE u.GB_consumed > (p.data_limit_GB * 0.9)
ORDER BY u.GB_consumed DESC;""")

rows = cursor.fetchall()
for row in rows:
    print(row)

#premium client that pays more than ARPU
print("Premiun Clients that pay more than ARPU")
cursor.execute("""SELECT c.name, c.surname, p.Plan_name, p.Plan_price
    FROM customer c
        JOIN Contracts con ON c.customer_id = con.customer_id
        JOIN Plans p ON con.Plan_id = p.Plan_id
            WHERE con.Status = 'Active'
            AND p.Plan_price > (SELECT AVG(p2.Plan_price)
        FROM Contracts con2
        JOIN Plans p2 ON con2.Plan_id = p2.Plan_id
    WHERE con2.Status = 'Active'
    )
ORDER BY p.Plan_price DESC;
""")

rows = cursor.fetchall()
for row in rows:
    print(row)