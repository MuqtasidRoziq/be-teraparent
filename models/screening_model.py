from config.config import db
from datetime import datetime

class Screening(db.Model):
    __tablename__ = "screenings"

    id = db.Column(db.String(36), primary_key=True)

    child_id = db.Column(
        db.String(36),
        db.ForeignKey("children.id"),
        nullable=False
    )

    status = db.Column(db.String(50))

    total_score = db.Column(db.Integer)

    adhd_indicator = db.Column(db.String(50))

    autism_indicator = db.Column(db.String(50))

    speech_delay_indicator = db.Column(db.String(50))

    screened_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    answers = db.relationship(
        "ScreeningAnswer",
        backref="screening",
        lazy=True,
        cascade="all, delete"
    )

class ScreeningQuestion(db.Model):
    __tablename__ = "screening_questions"

    id = db.Column(db.String(36), primary_key=True)

    domain = db.Column(db.String(50))

    question_text = db.Column(db.Text)

    answer_type = db.Column(db.String(30))

    order_num = db.Column(db.Integer)

    is_active = db.Column(db.Boolean, default=True)

class ScreeningAnswer(db.Model):
    __tablename__ = "screening_answers"

    id = db.Column(db.String(36), primary_key=True)

    screening_id = db.Column(
        db.String(36),
        db.ForeignKey("screenings.id"),
        nullable=False
    )

    question_id = db.Column(
        db.String(36),
        db.ForeignKey("screening_questions.id"),
        nullable=False
    )

    answer_value = db.Column(db.String(100))

    score = db.Column(db.Integer)

    question = db.relationship(
        "ScreeningQuestion"
    )