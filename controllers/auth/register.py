from flask import request, jsonify
from models.user import User, AuthLog
from config.config import db

def register():
    try:

        data = request.get_json()
        nama_lengkap = data.get("nama_lengkap")
        email = data.get("email")
        password = data.get("password")

        # VALIDASI
        if not nama_lengkap or not email or not password:
            return jsonify({
                "success": False,
                "message": "Semua field wajib diisi"
            }), 400

        # CEK EMAIL
        existing_user = User.cari_by_email(email)

        if existing_user:
            return jsonify({
                "success": False,
                "message": "Email sudah digunakan"
            }), 400

        # BUAT USER
        user = User(
            nama_lengkap=nama_lengkap,
            email=email.lower().strip()
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # AUTH LOG
        log = AuthLog(
            user_id=user.id,
            aksi="REGISTER",
            ip_address=request.remote_addr,
            info_device=request.user_agent.string,
            berhasil=True,
            keterangan="Register berhasil"
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Register berhasil",
            "data": user.ke_dict()
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500