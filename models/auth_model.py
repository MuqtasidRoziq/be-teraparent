from config.config import db
from datetime import datetime

class AuthLog(db.Model):
    __tablename__ = "auth_logs"

    id = db.Column(db.String(36), primary_key=True)

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id")
    )

    action = db.Column(db.String(50))
    ip_address = db.Column(db.String(100))
    device_info = db.Column(db.Text)
    success = db.Column(db.Boolean)

    logged_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class OTPToken(db.Model):
    __tablename__ = "otp_tokens"

    id = db.Column(db.String(36), primary_key=True)

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id")
    )

    token_hash = db.Column(db.Text)
    purpose = db.Column(db.String(50))
    expires_at = db.Column(db.DateTime)
    is_used = db.Column(db.Boolean, default=False)