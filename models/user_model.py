from uuid import uuid4
from datetime import datetime
from config.config import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    photo_url = db.Column(db.Text)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    face_embedding = db.Column(db.Text)
    face_login_enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # RELATIONSHIP
    children = db.relationship(
        "Child",
        backref="parent",
        lazy=True,
        cascade="all, delete"
    )

    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True
    )