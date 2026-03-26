import sqlite3 as lite
# define database path
db_path = 'data.db'
conn = lite.connect(db_path)
cursor = conn.cursor()

#lösche alle Einträge zum Schutz vor Duplikaten
cursor.execute("DROP TABLE IF EXISTS usage")
cursor.execute("DROP TABLE IF EXISTS Contracts")
cursor.execute("DROP TABLE IF EXISTS Plans")
cursor.execute("DROP TABLE IF EXISTS customer")


#SQL Befehle werden an Datenbank übergeben, falls diese noch nicht existieren
cursor.execute("""CREATE TABLE IF NOT EXISTS customer(
                         customer_id INTEGER PRIMARY KEY AUTOINCREMENT ,    --einzigartige id
                         name TEXT,
                         surname TEXT,
                         zip_code INTEGER,
                         registration_date DATE
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Plans(
                      Plan_id INTEGER PRIMARY KEY AUTOINCREMENT ,       --einzigartige id
                      Plan_name TEXT,
                      Plan_price DECIMAL(10,2),     --genau 2 Nachkommastellen
                      data_limit_GB INTEGER
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Contracts(
                    Contract_ID INTEGER PRIMARY KEY AUTOINCREMENT,      --einzigartige id
                    customer_id INTEGER,
                    Plan_id INTEGER,
                    Status TEXT, --'Active' or 'Canceled'
                    Device_Option TEXT, -- 'iPhone', 'Android' oder 'Sim-Only'
                    Start_date DATE,
                    FOREIGN KEY (customer_id) REFERENCES customer(customer_id), --Kontrolle, ob id valide ist
                    FOREIGN KEY (Plan_id) REFERENCES Plans(Plan_id)     --Kontrolle, ob id valide ist

);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS usage(
    Log_id INTEGER PRIMARY KEY AUTOINCREMENT ,      --einzigartige id
    Contract_id INTEGER,
    Billing_Month TEXT,
    GB_consumed DECIMAL(10, 2),     --genau 2 Nachkommastellen
    FOREIGN KEY (Contract_ID) REFERENCES Contracts(Contract_ID)     --Kontrolle, ob id valide ist
);""")

#Füllung der Tables
cursor.execute("""INSERT OR IGNORE INTO customer (name, surname, zip_code, registration_date) VALUES
                                                                      ('Max', 'Mustermann', 40474, '2022-01-15'),
                                                                      ('Erika', 'Schmidt', 40210, '2023-05-20'),
                                                                      ('Joshua', 'Testuser', 47623, '2024-02-10'),
                                                                      ('Lukas', 'Netzwerk', 50667, '2021-11-01'),
                                                                      ('Sarah', 'Online', 10115, '2023-12-01');""")

cursor.execute("""INSERT OR IGNORE INTO Plans (Plan_name, Plan_price, data_limit_GB) VALUES
                                                             ('GigaMobil XS', 29.99, 5),
                                                             ('GigaMobil S', 39.99, 12),
                                                             ('GigaMobil M', 49.99, 25),
                                                             ('GigaMobil L', 59.99, 50),
                                                             ('GigaMobil XL', 79.99, 999);""")

cursor.execute("""INSERT OR IGNORE INTO Contracts (customer_id, Plan_id, Status, Device_Option, Start_date) VALUES
                                                                                    (1, 2, 'Active', 'iPhone', '2022-01-15'),   -- Max hat GigaMobil S
                                                                                    (2, 1, 'Active', 'Sim-Only', '2023-05-20'), -- Erika hat GigaMobil XS
                                                                                    (3, 3, 'Active', 'Android', '2024-02-10'),  -- Joshua hat GigaMobil M
                                                                                    (4, 5, 'Canceled', 'iPhone', '2021-11-01'), -- Lukas hat gekündigt
                                                                                    (5, 2, 'Active', 'Android', '2023-12-01');  -- Sarah hat GigaMobil S""")

cursor.execute("""INSERT OR IGNORE INTO usage (Contract_id, Billing_Month, GB_consumed) VALUES
                                                                (1, '2026-03', 11.2), -- Max (Limit 12GB): Fast am Limit! -> Upselling Case
                                                                (2, '2026-03', 4.9),  -- Erika (Limit 5GB): Fast am Limit! -> Upselling Case
                                                                (3, '2026-03', 10.5), -- Joshua (Limit 25GB): Alles okay.
                                                                (5, '2026-03', 3.0);  -- Sarah (Limit 12GB): Nutzt wenig.""")

#Speicherung
conn.commit()
#Schließe die Connection um Speicher zu sparen
conn.close()





