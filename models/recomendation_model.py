from config.config import db

class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id = db.Column(db.String(36), primary_key=True)

    screening_id = db.Column(
        db.String(36),
        db.ForeignKey("screenings.id")
    )

    psychologist_id = db.Column(
        db.String(36),
        db.ForeignKey("psychologists.id")
    )

    therapy_notes = db.Column(db.Text)
    condition_type = db.Column(db.String(50))