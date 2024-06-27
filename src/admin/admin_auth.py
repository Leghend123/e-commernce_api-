from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import validators
import os
from src.constants.Http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from src.model import User
from src.extensions import db
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies, set_access_cookies, jwt_required, get_jwt_identity, unset_jwt_cookies


auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


# @auth.route('/admin', methods=['POST'])



# Login As Admin...................
@auth.post('/login')



# add new admin ..............



# refresh token ............................
@auth.get('/refresh_token')
@jwt_required(refresh=True)



# current admin..............
@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "username": user.username,
        "email": user.email
    }), HTTP_200_OK


# logout admin............


@auth.post('/logout')
def logout():
    response = make_response(jsonify({"msg": "logged out successfully"}))
    unset_jwt_cookies(response)
    return response
