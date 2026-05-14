from config.config import db
from datetime import datetime

class DailyActivity(db.Model):
    __tablename__ = "daily_activities"

    id = db.Column(db.String(36), primary_key=True)

    child_id = db.Column(
        db.String(36),
        db.ForeignKey("children.id"),
        nullable=False
    )

    title = db.Column(db.String(100))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    video_url = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer)
    is_completed = db.Column(db.Boolean, default=False)
    activity_date = db.Column(db.Date)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class ActivityRecommendation(db.Model):
    __tablename__ = "activity_recommendations"

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(100))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    video_url = db.Column(db.Text)
    target_condition = db.Column(db.String(50))
    min_age_months = db.Column(db.Integer)
    max_age_months = db.Column(db.Integer)