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
    
class NATO(db.Model):
    __tablename__ = "nato_alphabet"

    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(2), nullable=False)
    correct = db.Column(db.String(50), nullable=False)
    wrong1 = db.Column(db.String(50))
    wrong2 = db.Column(db.String(50))
    wrong3 = db.Column(db.String(50))
    wrong4 = db.Column(db.String(50))
    wrong5 = db.Column(db.String(50))
    wrong6 = db.Column(db.String(50))
    wrong7 = db.Column(db.String(50))
    wrong8 = db.Column(db.String(50))
    wrong9 = db.Column(db.String(50))

    def get_all_options(self):
        wrongs = [
            w for w in [
                self.wrong1, self.wrong2, self.wrong3, self.wrong4,
                self.wrong5, self.wrong6, self.wrong7, self.wrong8, self.wrong9
            ] if w
        ]
        return [self.correct] + wrongs