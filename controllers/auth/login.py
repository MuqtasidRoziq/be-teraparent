from flask import request, jsonify
from models.user import User, AuthLog
from config.config import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

def login():

    try:

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        # CEK USER
        user = User.cari_by_email(email)

        if not user:

            return jsonify({
                "success": False,
                "message": "Email tidak ditemukan"
            }), 404

        # CEK PASSWORD
        if not user.cek_password(password):

            log = AuthLog(
                user_id=user.id,
                aksi="LOGIN",
                ip_address=request.remote_addr,
                info_device=request.user_agent.string,
                berhasil=False,
                keterangan="Password salah"
            )

            db.session.add(log)
            db.session.commit()

            return jsonify({
                "success": False,
                "message": "Password salah"
            }), 401

        # JWT TOKEN
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=1)
        )

        # AUTH LOG
        log = AuthLog(
            user_id=user.id,
            aksi="LOGIN",
            ip_address=request.remote_addr,
            info_device=request.user_agent.string,
            berhasil=True,
            keterangan="Login berhasil"
        )

        db.session.add(log)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Login berhasil",
            "access_token": access_token,
            "user": user.ke_dict()
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500