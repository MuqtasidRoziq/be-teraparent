from config.config import db

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.String(36), primary_key=True)

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id")
    )

    psychologist_id = db.Column(
        db.String(36),
        db.ForeignKey("psychologists.id")
    )

    child_id = db.Column(
        db.String(36),
        db.ForeignKey("children.id")
    )

    booking_time = db.Column(db.DateTime)
    status = db.Column(db.String(30))
    notes = db.Column(db.Text)

    psychologist = db.relationship(
        "Psychologist"
    )

    child = db.relationship(
        "Child"
    )