import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Secret Key
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

    # Datenbank
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_filename = os.getenv("DATABASE_FILE", "dienstgrade.db")
    db_path = os.path.join(basedir, "..", db_filename)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialisierung
    db.init_app(app)
    from app import models

    # Blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Debug-Ausgabe
    if app.debug:
        print("Registrierte Routen:")
        print(app.url_map)

    return app