from . import db

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(50))           # Heer, Luftwaffe, Marine
    title = db.Column(db.String(100))
    abbreviation = db.Column(db.String(20))
    level_code = db.Column(db.String(20))
    rank_type = db.Column(db.String(50))        # Mannschaft, Unteroffizier, Offizier
    description = db.Column(db.Text)
    image_filename = db.Column(db.String(200))

    def __repr__(self):
        return f"<Rank {self.title}>"