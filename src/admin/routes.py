from src.constants.Http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import validators
import os
from src.constants.Http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from src.model import User
from src.extensions import db
from flask_jwt_extended import jwt_required
from .controllers import add_admin, login, refresh_user_token, current_admin, get_all_admin, logout


admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

# add new admin...............


@admin_bp.post("/create_new_admin")
@jwt_required()
def create_admin():
    try:
        response, status_code = add_admin()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# login as admin................


@admin_bp.post('/login')
def admin_login():
    try:
        response, status_code = login()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# refresh token..................


@admin_bp.get('/refresh_token')
@jwt_required(refresh=True)
def refresh_token():
    try:
        response, status_code = refresh_user_token()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# current admin...............
@admin_bp.get('/current_admin')
@jwt_required()
def admin():
    try:
        response, status_code = current_admin()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# logouut
def logout():
    try:
        response, status_code = logout()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# get all admin
@admin_bp.get('/all_admin')
@jwt_required()
def all_admin():
    try:
        response, status_code = get_all_admin()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR