from datetime import datetime
from config.config import db

class Screening(db.Model):
    __tablename__ = 'screenings'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'))
    indication = db.Column(db.String(50))
    total_score = db.Column(db.Integer) # Skor total untuk logika diagnosa
    domain_scores = db.Column(db.JSON) # Skor per domain (REQ-017)
    recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ScreeningQuestion(db.Model):
    __tablename__ = 'screening_questions'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    question_text = db.Column(db.Text, nullable=False)
    age_range = db.Column(db.String(20))
    points = db.Column(db.Integer, default=1)

class ScreeningAnswer(db.Model):
    __tablename__ = 'screening_answers'
    id = db.Column(db.Integer, primary_key=True)
    screening_id = db.Column(db.Integer, db.ForeignKey('screenings.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('screening_questions.id'))
    answer_value = db.Column(db.Boolean)