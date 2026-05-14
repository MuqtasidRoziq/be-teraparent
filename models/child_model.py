from config.config import db
from datetime import datetime

class Child(db.Model):
    __tablename__ = "children"

    id = db.Column(db.String(36), primary_key=True)

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    name = db.Column(db.String(100), nullable=False)
    age_months = db.Column(db.Integer)
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    gender = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # RELATIONSHIP
    screenings = db.relationship(
        "Screening",
        backref="child",
        lazy=True
    )

    activities = db.relationship(
        "DailyActivity",
        backref="child",
        lazy=True
    )

    child_progress = db.relationship(
        "ChildProgress",
        backref="child",
        lazy=True
    )

class ChildProgress(db.Model):
    __tablename__ = "child_progress"

    id = db.Column(db.String(36), primary_key=True)

    child_id = db.Column(
        db.String(36),
        db.ForeignKey("children.id"),
        nullable=False
    )

    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    recorded_date = db.Column(db.Date)
    notes = db.Column(db.Text)    