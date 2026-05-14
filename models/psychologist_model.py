from config.config import db

class Psychologist(db.Model):
    __tablename__ = "psychologists"

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    rating = db.Column(db.Float)
    photo_url = db.Column(db.Text)
    schedule_info = db.Column(db.Text)