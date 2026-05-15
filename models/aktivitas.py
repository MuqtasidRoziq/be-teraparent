from datetime import date, timedelta
from base_model import ModelDasar
from config.config import db


class TemplateAktivitas(ModelDasar):
    __tablename__ = "activity_templates"

    # ── Info Aktivitas ─────────────────────────────────────────────
    judul        = db.Column(db.String(150), nullable=False)
    kategori     = db.Column(db.String(50), nullable=False)
    url_video = db.Column(db.String(500), nullable=True)
    durasi_menit = db.Column(db.Integer, default=15)

    # ── Target Kondisi ─────────────────────────────────────────────
    # Aktivitas ini cocok untuk kondisi apa?
    untuk_kondisi = db.Column(db.String(50), nullable=False)

    # ── Filter Usia ────────────────────────────────────────────────
    min_usia_bulan = db.Column(db.Integer, nullable=False)
    max_usia_bulan = db.Column(db.Integer, nullable=False)
    is_aktif = db.Column(db.Boolean, default=True)

    # Relasi
    aktivitas_anak = db.relationship("Aktivitas", backref="template", lazy=True)

    @classmethod
    def cari_untuk_anak(cls, kondisi: str, usia_bulan: int):
        """
        Cari template yang sesuai dengan kondisi dan usia anak.
        Dipakai oleh recommendation_service untuk buat aktivitas rekomendasi.
        """
        return cls.query.filter(
            cls.untuk_kondisi.in_([kondisi, "umum"]),
            cls.min_usia_bulan <= usia_bulan,
            cls.max_usia_bulan >= usia_bulan,
            cls.is_aktif == True
        ).all()

    def ke_dict(self):
        return {
            "id": self.id,
            "judul": self.judul,
            "kategori": self.kategori,
            "deskripsi": self.deskripsi,
            "url_video": self.url_video,
            "durasi_menit": self.durasi_menit,
            "untuk_kondisi": self.untuk_kondisi,
        }


# ══════════════════════════════════════════════════════════════════════
#  TABEL: activities
#  Aktivitas yang ditugaskan untuk anak tertentu.
#  Dibuat otomatis setelah screening selesai (oleh recommendation_service).
#  Orang tua menandai "selesai" setelah aktivitas dilakukan.
#  Data ini yang dipakai untuk GRAFIK PROGRES AKTIVITAS.
# ══════════════════════════════════════════════════════════════════════
class Aktivitas(ModelDasar):
    __tablename__ = "activities"

    anak_id = db.Column(db.String(36), db.ForeignKey("children.id"))
    template_id = db.Column(db.String(36), db.ForeignKey("activity_templates.id"), nullable=True)

    # ── Info Aktivitas ─────────────────────────────────────────────
    # Disalin dari template saat dibuat, agar tetap konsisten
    # meskipun template diubah di kemudian hari
    judul = db.Column(db.String(150), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    url_video = db.Column(db.String(500), nullable=True)
    durasi_menit = db.Column(db.Integer, default=15)

    # ── Status Penyelesaian ────────────────────────────────────────
    sudah_selesai = db.Column(db.Boolean, default=False)
    tanggal_aktivitas = db.Column(db.Date, nullable=False, default=date.today)
    tanggal_selesai = db.Column(db.Date, nullable=True,)

    @classmethod
    def ambil_by_anak(cls, anak_id: str, hanya_belum_selesai: bool = False):
        """Ambil semua aktivitas anak, bisa filter yang belum selesai saja."""
        query = cls.query.filter_by(anak_id=anak_id)
        if hanya_belum_selesai:
            query = query.filter_by(sudah_selesai=False)
        return query.order_by(cls.tanggal_aktivitas.asc()).all()

    @classmethod
    def hitung_progres_minggu_ini(cls, anak_id: str) -> dict:
        """
        Hitung persentase aktivitas yang selesai minggu ini.
        Dipakai untuk ditampilkan di halaman home.
        """
        awal_minggu = date.today() - timedelta(days=date.today().weekday())
        akhir_minggu = awal_minggu + timedelta(days=6)

        semua = cls.query.filter(
            cls.anak_id == anak_id,
            cls.tanggal_aktivitas >= awal_minggu,
            cls.tanggal_aktivitas <= akhir_minggu,
        ).all()

        if not semua:
            return {"total": 0, "selesai": 0, "persen": 0}

        selesai = sum(1 for a in semua if a.sudah_selesai)
        return {
            "total": len(semua),
            "selesai": selesai,
            "persen": round((selesai / len(semua)) * 100),
        }

    def ke_dict(self):
        return {
            "id": self.id,
            "anak_id": self.anak_id,
            "judul": self.judul,
            "kategori": self.kategori,
            "deskripsi": self.deskripsi,
            "url_video": self.url_video,
            "durasi_menit": self.durasi_menit,
            "sudah_selesai": self.sudah_selesai,
            "tanggal_aktivitas": self.tanggal_aktivitas.isoformat(),
            "tanggal_selesai": self.tanggal_selesai.isoformat() if self.tanggal_selesai else None,
        }
