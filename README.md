# Telco_Data_Visualization 📊

Ein Python-basiertes Analysetool für Telekommunikationsdaten. Dieses Projekt automatisiert die Verwaltung einer SQLite-Datenbank, berechnet wichtige Geschäftskennzahlen (KPIs) und visualisiert Umsatzdaten nach Standorten.

## 🚀 Funktionen

* **Automatisierter Datenimport:** Effizientes Befüllen der Datenbank über ein separates Skript.
* **Dublettenschutz:** Intelligente Speicherlogik verhindert doppelte Datensätze in der Datenbank.
* **ARPU-Analyse:** Berechnung des *Average Revenue Per User* zur Messung der Profitabilität.
* **Upselling-Identifikation:** Analyse des Datenverbrauchs, um Kunden mit Upgrade-Potential (nahe am Datenlimit) zu finden.
* **Geografische Visualisierung:** Generierung von Säulendiagrammen zur Darstellung der Umsätze nach Postleitzahl (ZIP-Code).

## 🛠 Installation & Setup

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/jos2k4/Telco_Data_Visualization.git
    cd Telco_Data_Visualization
    ```

2.  **Abhängigkeiten installieren:**
    Stelle sicher, dass `pandas` und `matplotlib` installiert sind:
    ```bash
    pip install pandas matplotlib
    ```

## 📖 Bedienungsanleitung

> [!IMPORTANT]
> Bitte das Programm **nur über die `main.py` starten**. 

Der Workflow ist intern wie folgt strukturiert:
1.  **Initialisierung:** Beim Start der `main.py` werden die Daten automatisch über `fill_db.py` in die lokale `data.db` geladen.
2.  **Validierung:** Bestehende Daten werden geprüft, um eine doppelte Speicherung zu vermeiden.
3.  **Analyse:** Die Kennzahlen werden berechnet und in der Konsole ausgegeben.
4.  **Visualisierung:** Ein Fenster mit der Umsatzgrafik öffnet sich automatisch.

## 📊 Datenmodell

Die Datenbank (`data.db`) umfasst folgende Relationen:
* `customer`: Stammdaten der Nutzer.
* `Plans`: Tarifdetails (Preis, Datenvolumen).
* `Contracts`: Verknüpfung von Kunden mit Tarifen und Geräten.
* `usage`: Monatlicher Datenverbrauch pro Vertrag.

## 📈 KPI Definitionen

* **ARPU ($Average\ Revenue\ Per\ User$):**
    $$ARPU = \frac{\sum \text{Plan\_Price}}{\text{Anzahl aktive Kunden}}$$
* **Upgrade-Logik:** Kunden werden markiert, wenn ihr Verbrauch $GB\_consumed > 80\%$ des Tariflimits erreicht.

---

**Möchtest du, dass ich noch einen Abschnitt "Lizenz" oder "Mitwirkende" hinzufüge?**
