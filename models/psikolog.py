from config.config import db

class Psychologist(db.Model):
    __tablename__ = 'psychologists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50))
    specialization = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    photo_url = db.Column(db.String(255))
    rating = db.Column(db.Float, default=0.0)
    consultation_fee = db.Column(db.Float)
    practice_schedule = db.Column(db.JSON)
    
    sessions = db.relationship('Consultation', backref='doctor', lazy=True)

class Consultation(db.Model):
    __tablename__ = 'consultations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    psychologist_id = db.Column(db.Integer, db.ForeignKey('psychologists.id'), nullable=False)
    
    status = db.Column(db.String(20), default='pending') 
    booking_date = db.Column(db.DateTime, nullable=False)
    meeting_link = db.Column(db.String(255))
    notes_from_psychologist = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())