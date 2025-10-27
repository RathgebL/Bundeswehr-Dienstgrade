import csv
import os
import sys

# Absoluter Pfad zum Projektstamm ermitteln
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# --- Flask-App importieren ---
from app import create_app, db
from app.models import NATO

def import_nato_alphabet(csv_path="data/nato_alphabet.csv"):
    # Importiert NATO-Alphabet aus der CSV-Datei in die SQLite-Datenbank
    app = create_app()

    # App-Kontext aktivieren
    with app.app_context():
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            imported = 0

            for row in reader:
                entry = NATO(
                    letter=row["letter"].strip(),
                    correct=row["correct"].strip(),
                    wrong1=row.get("wrong1", "").strip(),
                    wrong2=row.get("wrong2", "").strip(),
                    wrong3=row.get("wrong3", "").strip(),
                    wrong4=row.get("wrong4", "").strip(),
                    wrong5=row.get("wrong5", "").strip(),
                    wrong6=row.get("wrong6", "").strip(),
                    wrong7=row.get("wrong7", "").strip(),
                    wrong8=row.get("wrong8", "").strip(),
                    wrong9=row.get("wrong9", "").strip()
                )
                db.session.add(entry)
                imported += 1

            db.session.commit()
            print(f"{imported} Einträge aus dem NATO-Alphabet erfolgreich importiert.")


if __name__ == "__main__":
    import_nato_alphabet()