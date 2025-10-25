import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "nijagh7z325ibjdsf9"

    # Absoluter Pfad zur Datenbank im Hauptordner
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "..", "dienstgrade.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Datenbank initialisieren
    db.init_app(app)

    # Modelle importieren
    from app import models

    # Blueprint importieren & registrieren
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Debug
    print("Registrierte Routen:")
    print(app.url_map)

    return app