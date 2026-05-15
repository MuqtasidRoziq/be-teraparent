import bcrypt
from datetime import datetime
from base_model import ModelDasar, buat_uuid
from config.config import db

class User(ModelDasar):
    __tablename__ = "users"

    # ── Data Pribadi ───────────────────────────────────────────────
    nama_lengkap = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    google_id  = db.Column(db.String(100), nullable=True, unique=True)
    foto_profil = db.Column(db.String(500), nullable=True)

    # ── Login Wajah (Face Recognition) ────────────────────────────
    # Embedding = representasi wajah dalam bentuk angka (vektor 512 dimensi)
    # Disimpan sebagai teks JSON, contoh: "[0.12, -0.34, 0.89, ...]"
    embedding_wajah     = db.Column(db.Text, nullable=True)
    login_wajah_aktif   = db.Column(db.Boolean, default=False)

    # ── Status Akun ────────────────────────────────────────────────
    aktif = db.Column(db.Boolean, default=True,)
    anak_anak       = db.relationship("Anak", backref="pemilik", lazy=True, cascade="all, delete-orphan")
    refresh_tokens  = db.relationship("RefreshToken", backref="pengguna", lazy=True, cascade="all, delete-orphan")
    otp_tokens      = db.relationship("OtpToken", backref="pengguna", lazy=True, cascade="all, delete-orphan")
    log_aktivitas   = db.relationship("AuthLog", backref="pengguna", lazy=True, cascade="all, delete-orphan")
    booking_saya    = db.relationship("Booking", backref="pengguna", lazy=True, cascade="all, delete-orphan")

    # ── Method: Password ───────────────────────────────────────────
    def set_password(self, password_asli: str):
        salt = bcrypt.gensalt(rounds=12)  # rounds=12 = cukup lambat untuk brute force
        self.password_hash = bcrypt.hashpw(
            password_asli.encode("utf-8"), salt
        ).decode("utf-8")

    def cek_password(self, password_asli: str) -> bool:
        if not self.password_hash:
            return False  # User login via Google, tidak punya password
        return bcrypt.checkpw(
            password_asli.encode("utf-8"),
            self.password_hash.encode("utf-8")
        )

    # ── Method: Cari Data ──────────────────────────────────────────
    @classmethod
    def cari_by_email(cls, email: str):
        return cls.query.filter_by(email=email.lower().strip()).first()

    @classmethod
    def cari_by_google_id(cls, google_id: str):
        return cls.query.filter_by(google_id=google_id).first()

    # ── Method: Ubah ke Dict (untuk response API) ──────────────────
    def ke_dict(self):
        """Ubah objek User menjadi dictionary untuk dikirim sebagai JSON."""
        return {
            "id":               self.id,
            "nama_lengkap":     self.nama_lengkap,
            "email":            self.email,
            "foto_profil":      self.foto_profil,
            "login_wajah_aktif": self.login_wajah_aktif,
            "dibuat_pada":      self.dibuat_pada.isoformat(),
        }


# ══════════════════════════════════════════════════════════════════════
#  TABEL: refresh_tokens
#  Menyimpan token refresh agar bisa di-nonaktifkan saat logout.
#  (Ini yang membuat logout benar-benar aman di sistem JWT)
# ══════════════════════════════════════════════════════════════════════
class RefreshToken(ModelDasar):
    __tablename__ = "refresh_tokens"

    user_id    = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    hash_token  = db.Column(db.String(255), nullable=False, unique=True)
    berlaku_sampai = db.Column(db.DateTime, nullable=False)
    sudah_dicabut  = db.Column(db.Boolean, default=False)


# ══════════════════════════════════════════════════════════════════════
#  TABEL: otp_tokens
#  Menyimpan kode OTP 6 digit untuk fitur reset password.
# ══════════════════════════════════════════════════════════════════════
class OtpToken(ModelDasar):
    __tablename__ = "otp_tokens"

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    hash_token = db.Column(db.String(255), nullable=False)
    tujuan = db.Column(db.String(50), nullable=False)
    berlaku_sampai = db.Column(db.DateTime, nullable=False)
    sudah_dipakai  = db.Column(db.Boolean, default=False)


# ══════════════════════════════════════════════════════════════════════
#  TABEL: auth_logs  ← WAJIB ADA (syarat dari evaluasi dosen)
#  Mencatat semua aktivitas login, logout, dan gagal login.
#  Berguna untuk audit keamanan dan deteksi percobaan hack.
# ══════════════════════════════════════════════════════════════════════
class AuthLog(db.Model):
    __tablename__ = "auth_logs"

    id = db.Column(db.String(36), primary_key=True, default=buat_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"),nullable=True)
    aksi = db.Column(db.String(50), nullable=False)
    ip_address  = db.Column(db.String(50), nullable=True)
    info_device = db.Column(db.String(255), nullable=True)
    berhasil = db.Column(db.Boolean, nullable=False)
    keterangan  = db.Column(db.String(255), nullable=True)
    dicatat_pada = db.Column(db.DateTime, default=datetime.utcnow)
