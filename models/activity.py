from config.config import db

class DailyActivity(db.Model):
    __tablename__ = 'daily_activities'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(255)) 
    category = db.Column(db.String(50))
    
    is_finished = db.Column(db.Boolean, default=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    completed_at = db.Column(db.DateTime)