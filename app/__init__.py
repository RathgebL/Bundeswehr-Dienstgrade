import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Absoluter Pfad zur Datenbank im Hauptordner
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "..", "dienstgrade.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app import models

    return app