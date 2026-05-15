from datetime import datetime
from base_model import ModelDasar
from config.config import db


# ══════════════════════════════════════════════════════════════════════
#  TABEL: psychologists
#  Menyimpan data psikiater/psikolog yang tampil di halaman pencarian.
#  Tabel ini diisi oleh admin aplikasi.
# ══════════════════════════════════════════════════════════════════════
class Psikiater(ModelDasar):
    __tablename__ = "psychologists"

    nama = db.Column(db.String(120), nullable=False)
    gelar = db.Column(db.String(100), nullable=True)
    spesialisasi = db.Column(db.String(150), nullable=False)
    pengalaman_tahun = db.Column(db.Integer, default=0)
    foto_url = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float, default=0.0)
    jumlah_ulasan = db.Column(db.Integer, default=0)
    info_jadwal = db.Column(db.Text, nullable=True)
    lokasi = db.Column(db.String(255), nullable=True)
    bisa_online = db.Column(db.Boolean, default=True)
    is_aktif = db.Column(db.Boolean, default=True)

    # Relasi 
    booking_list = db.relationship("Booking", backref="psikiater", lazy=True)
    rekomendasi_list = db.relationship("Rekomendasi", backref="psikiater", lazy=True)

    @classmethod
    def cari_aktif(cls, spesialisasi: str = None):
        """
        Ambil semua psikiater aktif.
        Bisa difilter berdasarkan spesialisasi tertentu.
        """
        query = cls.query.filter_by(is_aktif=True)
        if spesialisasi:
            # Filter yang spesialisasinya mengandung kata kunci
            query = query.filter(cls.spesialisasi.ilike(f"%{spesialisasi}%"))
        return query.order_by(cls.rating.desc()).all()

    def ke_dict(self):
        return {
            "id": self.id,
            "nama": self.nama,
            "gelar": self.gelar,
            "spesialisasi": self.spesialisasi,
            "pengalaman_tahun": self.pengalaman_tahun,
            "foto_url": self.foto_url,
            "rating": self.rating,
            "jumlah_ulasan": self.jumlah_ulasan,
            "info_jadwal": self.info_jadwal,
            "lokasi": self.lokasi,
            "bisa_online": self.bisa_online,
        }


# ══════════════════════════════════════════════════════════════════════
#  TABEL: bookings
#  Menyimpan data reservasi konsultasi.
#  Orang tua booking psikiater → psikiater konfirmasi → konsultasi.
# ══════════════════════════════════════════════════════════════════════
class Booking(ModelDasar):
    __tablename__ = "bookings"

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    psikiater_id = db.Column(db.String(36), db.ForeignKey("psychologists.id"), nullable=False)
    anak_id      = db.Column(db.String(36), db.ForeignKey("children.id"), nullable=False)
    waktu_booking = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="menunggu")
    jenis = db.Column(db.String(20), default="online")

    catatan = db.Column(db.Text, nullable=True)

    @classmethod
    def ambil_by_user(cls, user_id: str):
        """Ambil semua booking milik satu pengguna, dari yang terbaru."""
        return cls.query.filter_by(user_id=user_id).order_by(cls.waktu_booking.desc()).all()

    def ke_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "psikiater_id": self.psikiater_id,
            "anak_id": self.anak_id,
            "waktu_booking": self.waktu_booking.isoformat(),
            "status": self.status,
            "jenis": self.jenis,
            "catatan": self.catatan,
        }
