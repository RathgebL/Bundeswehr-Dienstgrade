from app import create_app, db
from app.models import Rank

app = create_app()

with app.app_context():
    db.create_all()
    print("SQLite-Datenbank 'dienstgrade.db' wurde erfolgreich angelegt!")