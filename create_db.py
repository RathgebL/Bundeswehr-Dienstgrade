from app import create_app, db
from app.models import Rank

# print("db id in create_db:", id(db)) #debug

app = create_app()
# print("DB path:", app.config["SQLALCHEMY_DATABASE_URI"]) #debug

with app.app_context():
    # print("Registrierte Tabellen:", db.Model.metadata.tables.keys()) #debug
    db.create_all()
    # print("Nach create_all():", db.Model.metadata.tables.keys()) #debug
    print("SQLite-Datenbank 'dienstgrade.db' wurde erfolgreich angelegt!")