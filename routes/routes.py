from flask import Blueprint, Flask
from flask_jwt_extended import jwt_required
from controllers.auth.register import register
from controllers.auth.login import login

api_auth_bp = Blueprint("api_auth", __name__, url_prefix='/api/auth')


@jwt_required()
@api_auth_bp.route("/register", methods=["POST"])
def api_register():
    return register()

@jwt_required()
@api_auth_bp.route("/login", methods=["POST", "GET"])
def api_login():
    return login()