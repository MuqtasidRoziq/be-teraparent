import uuid
from datetime import datetime
from config.config import db


def buat_uuid():
    return str(uuid.uuid4())


class ModelDasar(db.Model):
    """
    Class dasar yang diwarisi semua model.
    Otomatis punya kolom: id, dibuat_pada, diupdate_pada.
    """
    __abstract__ = True # Ini artinya SQLAlchemy TIDAK akan buat tabel untuk class ini

    id  = db.Column(db.String(36), primary_key=True, default=buat_uuid)
    dibuat_pada = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    diupdate_pada = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def simpan(self):
        """Simpan perubahan ke database."""
        db.session.add(self)
        db.session.commit()
        return self

    def hapus(self):
        """Hapus data dari database."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def cari_by_id(cls, id: str):
        """Cari satu data berdasarkan ID."""
        return cls.query.get(id)

    @classmethod
    def ambil_semua(cls):
        """Ambil semua data dari tabel."""
        return cls.query.all()
