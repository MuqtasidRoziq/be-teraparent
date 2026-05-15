# 1. Model akun & autentikasi (tidak bergantung model lain)
from .user import User, RefreshToken, OtpToken, AuthLog

# 2. Model anak (bergantung pada User)
from .anak import Anak, CatatanTumbuh

# 3. Model psikiater (tidak bergantung model lain)
from .psikiater import Psikiater, Booking

# 4. Model screening (bergantung pada Anak dan Psikiater)
from .screening import PertanyaanScreening, Screening, JawabanScreening, Rekomendasi

# 5. Model aktivitas (bergantung pada Anak)
from .aktivitas import TemplateAktivitas, Aktivitas


# ── Daftar semua tabel (untuk referensi) ──────────────────────────────
#
#  users                  → akun pengguna
#  refresh_tokens         → token JWT untuk logout aman
#  otp_tokens             → kode OTP reset password
#  auth_logs              → log semua aktivitas login (wajib ada)
#  children               → data profil anak
#  growth_records         → riwayat berat & tinggi (grafik fisik)
#  psychologists          → data psikiater
#  bookings               → reservasi konsultasi
#  screening_questions    → master soal kuesioner
#  screenings             → sesi pengisian kuesioner
#  screening_answers      → jawaban per soal
#  recommendations        → hasil rekomendasi psikiater & terapi
#  activity_templates     → master aktivitas terapi + video
#  activities             → aktivitas yang ditugaskan ke anak
#
# Total: 14 tabel
