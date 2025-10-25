import csv
from app import create_app, db
from app.models import Rank

app = create_app()

with app.app_context():
    with open("data/dienstgrade.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rank = Rank(**row)
            db.session.add(rank)
        db.session.commit()
    print("Daten importiert!")