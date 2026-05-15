from datetime import datetime
from .base_model import ModelDasar
from config.config import db


# ══════════════════════════════════════════════════════════════════════
#  TABEL: screening_questions = MASTER DATA SOAL
#  Berisi semua pertanyaan kuesioner yang sudah divalidasi secara klinis.
#  Admin/developer yang mengisi tabel ini satu kali (seed data).
#  Tidak perlu diubah kecuali ada update instrumen klinis.
# ══════════════════════════════════════════════════════════════════════
class PertanyaanScreening(db.Model):
    __tablename__ = "screening_questions"

    id = db.Column(db.String(36), primary_key=True) 
    domain = db.Column(db.String(50), nullable=False) # contoh: "social", "language", "motor", "behavior"
    sumber_instrumen = db.Column(db.String(50), nullable=False) # contoh: "M-CHAT", "SWYC", "CDC Milestone"
    teks_pertanyaan = db.Column(db.Text, nullable=False) # isi pertanyaan yang ditampilkan ke orang tua
    tipe_jawaban = db.Column(db.String(20), nullable=False) # contoh: "ya_tidak", "skala_1_5", "pilihan_ganda"

    # Aturan Skor 
    # Logika skor berbeda tergantung soal:
    # - "ya" bisa bernilai 0 atau 1 tergantung konteks pertanyaan
    # - is_kritis = True → soal yang bobotnya lebih berat (khusus M-CHAT)
    skor_jika_ya = db.Column(db.Integer, default=0)
    skor_jika_tidak = db.Column(db.Integer, default=0)
    is_kritis = db.Column(db.Boolean, default=False)

    # Filter Usia Anak
    min_usia_bulan = db.Column(db.Integer, nullable=False)
    max_usia_bulan = db.Column(db.Integer, nullable=False)

    # Urutan tampil 
    urutan = db.Column(db.Integer, default=0)
    is_aktif = db.Column(db.Boolean, default=True)

    # Relasi
    jawaban_list = db.relationship("JawabanScreening", backref="pertanyaan", lazy=True)

    @classmethod
    def ambil_by_usia(cls, usia_bulan: int):
        """
        Ambil semua soal yang sesuai untuk usia anak.
        Contoh: anak 24 bulan → ambil soal dengan min_usia <= 24 <= max_usia
        """
        return cls.query.filter(
            cls.min_usia_bulan <= usia_bulan,
            cls.max_usia_bulan >= usia_bulan,
            cls.is_aktif == True
        ).order_by(cls.domain, cls.urutan).all()

    def ke_dict(self):
        return {
            "id": self.id,
            "domain": self.domain,
            "sumber": self.sumber_instrumen,
            "pertanyaan": self.teks_pertanyaan,
            "tipe_jawaban": self.tipe_jawaban,
            "is_kritis": self.is_kritis,
        }


# ══════════════════════════════════════════════════════════════════════
#  TABEL: screenings
#  Satu baris = satu sesi pengisian kuesioner oleh orang tua.
#  Menyimpan RINGKASAN HASIL analisis setelah semua soal dijawab.
# ══════════════════════════════════════════════════════════════════════
class Screening(ModelDasar):
    __tablename__ = "screenings"

    anak_id = db.Column(db.String(36), db.ForeignKey("children.id"), nullable=False, index=True)

    # ── Status Pengisian ───────────────────────────────────────────
    status = db.Column(db.String(20), default="selesai")

    # ── Hasil Analisis Per Domain ──────────────────────────────────
    # Diisi otomatis oleh screening_service.py setelah semua soal dijawab
    # Nilai: 'rendah', 'sedang', 'tinggi'
    risiko_autisme = db.Column(db.String(10), nullable=True)
    risiko_adhd  = db.Column(db.String(10), nullable=True)
    risiko_speech_delay = db.Column(db.String(10), nullable=True)

    # Kondisi dengan risiko tertinggi = yang jadi fokus rekomendasi
    kondisi_utama = db.Column(db.String(30), nullable=True)

    tanggal_screening = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi
    jawaban_list = db.relationship("JawabanScreening", backref="screening", lazy=True, cascade="all, delete-orphan")
    rekomendasi_list = db.relationship("Rekomendasi",     backref="screening", lazy=True, cascade="all, delete-orphan")

    @classmethod
    def ambil_terakhir(cls, anak_id: str):
        """Ambil hasil screening paling baru untuk satu anak."""
        return cls.query.filter_by(anak_id=anak_id).order_by(cls.tanggal_screening.desc()).first()

    @classmethod
    def ambil_riwayat(cls, anak_id: str):
        """Ambil semua riwayat screening satu anak (dari terbaru)."""
        return cls.query.filter_by(anak_id=anak_id).order_by(cls.tanggal_screening.desc()).all()

    def ke_dict(self):
        return {
            "id": self.id,
            "anak_id": self.anak_id,
            "status": self.status,
            "risiko_autisme": self.risiko_autisme,
            "risiko_adhd": self.risiko_adhd,
            "risiko_speech_delay": self.risiko_speech_delay,
            "kondisi_utama": self.kondisi_utama,
            "tanggal_screening": self.tanggal_screening.isoformat(),
        }


# ══════════════════════════════════════════════════════════════════════
#  TABEL: screening_answers
#  Menyimpan jawaban SATU PER SATU soal dari satu sesi screening.
#  Contoh: satu screening dengan 20 soal → 20 baris di tabel ini.
# ══════════════════════════════════════════════════════════════════════
class JawabanScreening(ModelDasar):
    __tablename__ = "screening_answers"

    screening_id = db.Column(db.String(36), db.ForeignKey("screenings.id"), nullable=False, index=True)
    pertanyaan_id = db.Column(db.String(36), db.ForeignKey("screening_questions.id"), nullable=False)
    nilai_jawaban = db.Column(db.String(20), nullable=False)
    skor = db.Column(db.Integer, nullable=False, default=0)

    def ke_dict(self):
        return {
            "pertanyaan_id": self.pertanyaan_id,
            "jawaban": self.nilai_jawaban,
            "skor": self.skor,
        }


# ══════════════════════════════════════════════════════════════════════
#  TABEL: recommendations
#  Menyimpan hasil rekomendasi setelah screening selesai.
#  Berisi: psikiater yang disarankan + terapi yang bisa dilakukan di rumah.
# ══════════════════════════════════════════════════════════════════════
class Rekomendasi(ModelDasar):
    __tablename__ = "recommendations"

    screening_id = db.Column(db.String(36), db.ForeignKey("screenings.id"), nullable=False, index=True)
    psikiater_id = db.Column(db.String(36), db.ForeignKey("psychologists.id"),nullable=True)

    # Jenis kondisi yang mendasari rekomendasi ini
    untuk_kondisi = db.Column(db.String(30), nullable=False)

    # Saran terapi yang bisa dilakukan orang tua di rumah
    # Nanti terhubung ke fitur aktivitas
    catatan_terapi = db.Column(db.Text, nullable=True)

    def ke_dict(self):
        return {
            "id": self.id,
            "screening_id": self.screening_id,
            "psikiater_id": self.psikiater_id,
            "untuk_kondisi": self.untuk_kondisi,
            "catatan_terapi": self.catatan_terapi,
        }