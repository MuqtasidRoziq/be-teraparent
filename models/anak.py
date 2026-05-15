from datetime import date, datetime
from base_model import ModelDasar
from config.config import db


# ══════════════════════════════════════════════════════════════════════
#  TABEL: children
#  Satu akun pengguna BISA punya lebih dari satu anak.
#  Semua fitur (screening, aktivitas, grafik) terhubung ke anak,
#  bukan langsung ke akun pengguna.
# ══════════════════════════════════════════════════════════════════════
class Anak(ModelDasar):
    __tablename__ = "children"

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    nama = db.Column(db.String(100), nullable=False)
    usia_bulan = db.Column(db.Integer, nullable=False)
    tinggi_cm = db.Column(db.Float, nullable=False)
    berat_kg = db.Column(db.Float, nullable=False)
    jenis_kelamin = db.Column(db.String(10), nullable=False)

    catatan_tumbuh = db.relationship("CatatanTumbuh", backref="anak", lazy=True, cascade="all, delete-orphan", order_by="CatatanTumbuh.tanggal_catat.asc()")
    screening_list = db.relationship("Screening", backref="anak", lazy=True, cascade="all, delete-orphan")
    aktivitas_list = db.relationship("Aktivitas", backref="anak", lazy=True, cascade="all, delete-orphan")
    booking_list   = db.relationship("Booking", backref="anak", lazy=True, cascade="all, delete-orphan")

    # Method: Hitung Usia
    @property
    def usia_tahun(self) -> str:
        """
        Ubah usia bulan menjadi format yang lebih mudah dibaca.
        Contoh: 30 bulan → "2 tahun 6 bulan"
        """
        tahun = self.usia_bulan // 12
        bulan = self.usia_bulan % 12
        if tahun == 0:
            return f"{bulan} bulan"
        if bulan == 0:
            return f"{tahun} tahun"
        return f"{tahun} tahun {bulan} bulan"

    @classmethod
    def ambil_by_user(cls, user_id: str):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def cari_by_id_dan_user(cls, anak_id: str, user_id: str):
        return cls.query.filter_by(id=anak_id, user_id=user_id).first() # Cari anak berdasarkan ID dan pastikan anak itu milik user yang sedang login

    def ke_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "usia_bulan": self.usia_bulan,
            "usia_tampil": self.usia_tahun,
            "tinggi_cm": self.tinggi_cm,
            "berat_kg": self.berat_kg,
            "jenis_kelamin": self.jenis_kelamin,
            "dibuat_pada": self.dibuat_pada.isoformat(),
        }


# ══════════════════════════════════════════════════════════════════════
#  TABEL: growth_records
#  Menyimpan riwayat berat & tinggi dari waktu ke waktu.
#  Data ini yang dipakai untuk menggambar GRAFIK PERKEMBANGAN FISIK.
#
#  Cara kerja:
#  - Setiap kali orang tua input berat/tinggi terbaru → tambah record baru
#  - Grafik ditarik dari semua record yang ada, diurutkan berdasarkan tanggal
# ══════════════════════════════════════════════════════════════════════
class CatatanTumbuh(ModelDasar):
    __tablename__ = "growth_records"

    anak_id = db.Column(db.String(36), db.ForeignKey("children.id"), nullable=False, index=True)
    tinggi_cm = db.Column(db.Float, nullable=False, comment="Tinggi badan saat pencatatan (cm)")
    berat_kg = db.Column(db.Float, nullable=False, comment="Berat badan saat pencatatan (kg)")
    tanggal_catat = db.Column(db.Date, nullable=False, default=date.today, comment="Tanggal pengukuran dilakukan")
    catatan = db.Column(db.String(255), nullable=True, comment="Catatan opsional dari orang tua")

    @classmethod
    def ambil_riwayat(cls, anak_id: str):
        """Ambil semua riwayat tumbuh anak, diurutkan dari yang terlama."""
        return cls.query.filter_by(anak_id=anak_id).order_by(cls.tanggal_catat.asc()).all()

    def ke_dict(self):
        return {
            "id": self.id,
            "anak_id": self.anak_id,
            "tinggi_cm": self.tinggi_cm,
            "berat_kg": self.berat_kg,
            "tanggal_catat": self.tanggal_catat.isoformat(),
            "catatan": self.catatan,
        }
