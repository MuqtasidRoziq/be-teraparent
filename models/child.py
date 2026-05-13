import datetime

from config.config import db

class Child(db.Model):
    __tablename__ = 'children'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    
    # Relasi ke tabel-tabel pendukung
    growth_records = db.relationship('GrowthRecord', backref='child', lazy=True, cascade="all, delete-orphan")
    activities = db.relationship('DailyActivity', backref='child', lazy=True, cascade="all, delete-orphan")
    screenings = db.relationship('Screening', backref='child', lazy=True, cascade="all, delete-orphan")

class GrowthRecord(db.Model):
    __tablename__ = 'growth_records'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    weight = db.Column(db.Float) 
    height = db.Column(db.Float)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)