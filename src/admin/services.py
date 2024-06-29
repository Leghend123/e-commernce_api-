from ..model import User
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import validators
import os
from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies, set_access_cookies, get_jwt_identity, unset_jwt_cookies
from datetime import timedelta
from flask import jsonify, request, make_response
from src.constants.Http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED


class UserService:
    @staticmethod
    def default_admin():
        try:
            username = os.environ.get("USERNAME1")
            email = os.environ.get("EMAIL")
            password = os.environ.get("PASSWORD")
            profile = os.environ.get("PROFILE")

            if not validators.email(email):
                return jsonify({"error": "Invalid email format"}), 400

            if len(username) < 3:
                return jsonify({"error": "Username is too short"}), 400

            if len(password) < 6:
                return jsonify({"error": "Password is too short"}), 400

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"error": "Email already exists"}), 400

            # Hash password and create new user
            password_hash = generate_password_hash(password)
            admin = User(username=username, email=email,
                         password=password_hash, profile=profile)
            db.session.add(admin)
            db.session.commit()

            return jsonify({"msg": "User created successfully"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    # add new admin..........

    @staticmethod
    def add_admin(data):
        try:
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            profile = data.get("profile")

            if not validators.email(email):
                return {"error": "Invalid email"}, HTTP_400_BAD_REQUEST

            if len(username) < 3:
                return {"error": "Username is too short"}, HTTP_400_BAD_REQUEST

            if User.query.filter_by(username=username).first() is not None:
                return {"error": "Username is taken"}, HTTP_400_BAD_REQUEST

            if User.query.filter_by(email=email).first() is not None:
                return {"error": "Email is taken"}, HTTP_400_BAD_REQUEST

            if not username.isalnum() or " " in username:
                return {"error": "Username must be alphanumeric"}, HTTP_400_BAD_REQUEST

            if len(password) < 6:
                return {"error": "Password is too short"}, HTTP_400_BAD_REQUEST

            password_hash = generate_password_hash(password)

            user = User(username=username, email=email,
                        password=password_hash, profile=profile)
            db.session.add(user)
            db.session.commit()

            return {"msg": "New admin added"}, HTTP_201_CREATED

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def login(data):
        try:
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                if access_token and refresh_token:
                    access_max_age = timedelta(minutes=12)
                    refresh_max_age = timedelta(days=30)
                    response = make_response({"msg": 'login sucessfully'})
                    set_access_cookies(response, access_token,
                                       max_age=access_max_age,)
                    set_refresh_cookies(
                        response, refresh_token, max_age=refresh_max_age)

                return {
                    'user': {
                        'Refresh': refresh_token,
                        'Access': access_token,
                    }

                }, HTTP_200_OK
            else:
                return {'error': 'Invalid username or password'}, HTTP_400_BAD_REQUEST

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    # refesh token........................
    @staticmethod
    def refresh_user_token():

        identity = get_jwt_identity()
        access = create_access_token(identity=identity)
        response = make_response({"msg": "refreshed"})
        set_access_cookies(response, access)
        return {
            "access": access
        }, HTTP_200_OK

    # current admin .....................
    @staticmethod
    def current_admin():
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        return {
            "username": user.username,
            "email": user.email
        }, HTTP_200_OK

    # logout...........
    @staticmethod
    def logout():
        response = make_response({"msg": "logged out successfully"})
        unset_jwt_cookies(response)
        return response

    # get all admins

    @staticmethod
    def get_all_admin():
        users = User.query.filter_by().all()
        data = []
        for user in users:
            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile": user.profile

            })
        return {'data': data}, HTTP_200_OK
