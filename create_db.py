"""
Erstellt die SQLite-Datenbank (dienstgrade.db) mit allen Tabellen.
Diese Datei kann einmalig beim Setup oder nach Schemaänderungen ausgeführt werden.
"""

import os
from app import create_app, db
from app.models import Rank, NATO  # wichtig: alle Models importieren, damit sie registriert werden


def create_database():
    """Erstellt die SQLite-Datenbank mit allen Tabellen."""
    app = create_app()

    # Absoluten Pfad zur Datenbank anzeigen (zur Kontrolle)
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
    print(f"→ Datenbankpfad: {db_path}")

    # Sicherstellen, dass der Ordner existiert
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Tabellen anlegen
    with app.app_context():
        db.create_all()
        print("Alle Tabellen erfolgreich erstellt bzw. überprüft.")

        # Kontrolle: welche Tabellen existieren
        print("Registrierte Tabellen:")
        for table in db.metadata.tables.keys():
            print(f"   - {table}")

    print("SQLite-Datenbank wurde erfolgreich initialisiert!")


if __name__ == "__main__":
    create_database()