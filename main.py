import subprocess

#user Daten werden automatisch von der file fill_db.py in die Datenbank gespeichert. Bestehende Daten können nicht doppelt gespeichert werden.

#Programm bitte nur über die main.py starten. Die Daten werden ausgewerten, der ARPU wird berechnet,
# Kunden mit Upgrade Potential werden genannt und zum Schluss werden die Umsätze nach Standort in einem Säulendiagramm visualisiert

process1 = subprocess.Popen(["python", "fill_db.py"])
process2 = subprocess.Popen(["python", "evaluation.py"])
process3 = subprocess.Popen(["python", "visualization.py"])

process1.wait()
process2.wait()
process3.wait()


