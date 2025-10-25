from flask_sqlalchemy import SQLAlchemy
from . import db

# print("db id in models:", id(db)) #debug

class Rank(db.Model):
    __tablename__ = "rank"

    id = db.Column(db.Integer, primary_key=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    branch = db.Column(db.String(50))               # Heer, Luftwaffe, Marine
    title = db.Column(db.String(100))
    abbreviation = db.Column(db.String(20))
    level_code = db.Column(db.String(10))
    rank_type = db.Column(db.String(50))            # Mannschaft, Unteroffizier, Offizier
    rank_group = db.Column(db.String(100))          # Offizier: Leutnante und Hauptleute, Stabsoffiziere, Generale
    specialization = db.Column(db.String(50))       # Sanitäter
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(200))

    def __repr__(self):
        return f"<Rank {self.branch} - {self.title}>"