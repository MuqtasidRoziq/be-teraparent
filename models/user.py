from config.config import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_photo = db.Column(db.String(255))
    
    otp_code = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)
    new_email_pending = db.Column(db.String(120))
    face_embedding = db.Column(db.Text) 
    
    # Tambahkan cascade agar data bersih saat user hapus akun
    children = db.relationship('Child', backref='parent', lazy=True, cascade="all, delete-orphan")
    logs = db.relationship('AuditLog', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))