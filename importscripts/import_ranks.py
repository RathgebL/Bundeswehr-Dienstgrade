import csv
from app import create_app, db
from app.models import Rank

# Flask-App initialisieren (damit SQLAlchemy funktioniert)
app = create_app()

def import_ranks(csv_path="data/dienstgrade.csv"):
    """Importiert Dienstgrade aus der CSV-Datei in die SQLite-Datenbank."""
    with app.app_context():
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            imported = 0

            for row in reader:
                try:
                    rank = Rank(
                        sort_order=int(row.get("sort_order", 0) or 0),
                        branch=row.get("branch", "").strip(),
                        title=row.get("title", "").strip(),
                        abbreviation=row.get("abbreviation", "").strip(),
                        level_code=row.get("level_code", "").strip(),
                        rank_type=row.get("rank_type", "").strip(),
                        rank_group=row.get("rank_group", "").strip(),
                        specialization=row.get("specialization", "").strip(),
                        description=row.get("description", "").strip(),
                        image_filename=row.get("image_filename", "").strip()
                    )
                    db.session.add(rank)
                    imported += 1
                except Exception as e:
                    print(f"Fehler bei Zeile: {row}")
                    print(e)

            db.session.commit()
            print(f"{imported} Dienstgrade erfolgreich importiert!")
        

if __name__ == "__main__":
    import_ranks()