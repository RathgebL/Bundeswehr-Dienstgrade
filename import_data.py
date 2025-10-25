import csv
from app import create_app, db
from app.models import Rank

app = create_app()

with app.app_context():
    with open("data/dienstgrade.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rank = Rank(
                sort_order=int(row.get("sort_order", 0)),
                branch=row["branch"],
                title=row["title"],
                abbreviation=row["abbreviation"],
                level_code=row["level_code"],
                rank_type=row["rank_type"],
                rank_group=row["rank_group"],
                specialization=row["specialization"],
                description=row["description"],
                image_filename=row["image_filename"]
            )
            db.session.add(rank)
        db.session.commit()
        print("CSV-Daten erfolgreich in SQLite importiert!")