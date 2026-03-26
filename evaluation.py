import sqlite3 as lite
# Name der Datei
db_path = 'data.db'
#Datei wird geladen
conn = lite.connect(db_path)
#curser definiert
cursor = conn.cursor()

print("\n--- Auswertung abgeschlossen ---")
print("PLZ nach Umsatz:")

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
print("Average Revenue Per User:")

#Logik: ARPU = Gesamterlös / Anzahl Aktiver Kunden
cursor.execute("""SELECT AVG(p.Plan_price) AS ARPU
    FROM Contracts con
        JOIN Plans p ON con.Plan_id = p.Plan_id
WHERE con.Status = 'Active';""")        #Kunde muss aktiv sein

rows = cursor.fetchall()
#printen alle rows
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
WHERE u.GB_consumed > (p.data_limit_GB * 0.9)       --Vergleich zwischen verbrauchten Volumen und 90% des verfügbaren
ORDER BY u.GB_consumed DESC;""")

rows = cursor.fetchall()
#printen alle rows
for row in rows:
    print(row)

#premium client that pays more than ARPU
print("Premium Clients that pay more than ARPU")
cursor.execute("""SELECT c.name, c.surname, p.Plan_name, p.Plan_price
    FROM customer c
        JOIN Contracts con ON c.customer_id = con.customer_id
        JOIN Plans p ON con.Plan_id = p.Plan_id
            WHERE con.Status = 'Active'         --bis hier wurde der ARPU von allen Aktiven Kunden berechnet
            AND p.Plan_price > (SELECT AVG(p2.Plan_price)       --ARPU wird mit jedem Kunden verglichen, nur wer höher ist kommt weiter
        FROM Contracts con2
        JOIN Plans p2 ON con2.Plan_id = p2.Plan_id
    WHERE con2.Status = 'Active'                    --Überprüfung, ob Kunde aktiv ist
    )
ORDER BY p.Plan_price DESC;
""")

rows = cursor.fetchall()
#printet alle rows
for row in rows:
    print(row)


#Logik: Wenn 60% oder weniger des Datenvolumens verbraucht werden, dann gilt dieser Kunde als High-Risk-Customer

print("High-Risk-Customers")
cursor.execute("""SELECT
    c.name, c.surname, u.GB_consumed, p.data_limit_GB, p.Plan_name

FROM customer c
    JOIN Contracts con ON c.customer_id = con.customer_id
    JOIN Plans p ON con.Plan_id = p.Plan_id
    JOIN usage u ON con.Contract_id = u.Contract_id
WHERE u.GB_consumed < (p.data_limit_GB * 0.6)       --verbrauchtes Volumen wird mit 60% des Maximalvolumen verglichen
ORDER BY u.GB_consumed DESC;""")

rows = cursor.fetchall()
#printet alle rows
for row in rows:
    print(row)