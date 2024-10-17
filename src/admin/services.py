from ..model import User, Category,Product
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import validators
import os
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_refresh_cookies,
    set_access_cookies,
    get_jwt_identity,
    unset_jwt_cookies,
)
from datetime import timedelta
from flask import jsonify, request, make_response
from src.constants.Http_status_code import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)


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
            admin = User(
                username=username, email=email, password=password_hash, profile=profile
            )
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

            user = User(
                username=username, email=email, password=password_hash, profile=profile
            )
            db.session.add(user)
            db.session.commit()

            return {"msg": "New admin added"}, HTTP_201_CREATED

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def login(data):
        try:
            username = data.get("username")
            password = data.get("password")

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                if access_token and refresh_token:
                    access_max_age = timedelta(minutes=12)
                    refresh_max_age = timedelta(days=30)
                    response = make_response({"msg": "login sucessfully"})
                    set_access_cookies(
                        response,
                        access_token,
                        max_age=access_max_age,
                    )
                    set_refresh_cookies(
                        response, refresh_token, max_age=refresh_max_age
                    )

                return {
                    "user": {
                        "Refresh": refresh_token,
                        "Access": access_token,
                    }
                }, HTTP_200_OK
            else:
                return {"error": "Invalid username or password"}, HTTP_400_BAD_REQUEST

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    # refesh token........................
    @staticmethod
    def refresh_user_token():

        identity = get_jwt_identity()
        access = create_access_token(identity=identity)
        response = make_response({"msg": "refreshed"})
        set_access_cookies(response, access)
        return {"access": access}, HTTP_200_OK

    # current admin .....................
    @staticmethod
    def current_admin():
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        return {"username": user.username, "email": user.email}, HTTP_200_OK

    # logout...........
    @staticmethod
    def logout():
        response = make_response({"msg": "logged out successfully"})
        unset_jwt_cookies(response)
        return response

    # get all admins

    @staticmethod
    def get_all_admin():
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_pagge", 5, type=int)
        users = User.query.filter_by().paginate(page=page, per_page=per_page)
        data = []
        for user in users:
            data.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "profile": user.profile,
                }
            )
        meta = {
            "page": users.page,
            "pages": users.pages,
            "total_count": users.total,
            "prev_page": users.prev_num,
            "next_page": users.next_num,
            "has_next": users.has_next,
            "has_prev": users.has_prev,
        }
        return {"data": data, "meta": meta}, HTTP_200_OK

    @staticmethod
    def get_admin_by_id(id):
        admin = User.query.filter_by(id=id).first()
        if not admin:
            return {"Error": "No Admin found!"}, HTTP_404_NOT_FOUND
        return {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
            "created_at": admin.created_at,
        }, HTTP_200_OK

    @staticmethod
    def delete_admin(id):
        admin = User.query.filter_by(id=id).first()
        if not admin:
            return {"error": "admin not found!"}, HTTP_404_NOT_FOUND

        db.session.delete(admin)
        db.session.commit()

        return {"msg": "deleted successfully"}, HTTP_200_OK

    @staticmethod
    def edit_admin(id):
        admin = User.query.filter_by(id=id).first()
        if not admin:
            return {"error": "admin not found!"}, HTTP_404_NOT_FOUND

        username = request.get_json().get("username", "")

        if not username.isalnum() or " " in username:
            return {"error": "Username must be alphanumeric"}, HTTP_400_BAD_REQUEST
        if len(username) < 3:
            return {"error": "username too short!"}, HTTP_400_BAD_REQUEST

        admin.username = username
        db.session.commit()
        return {"error": "admin editted successfully!"}, HTTP_200_OK


# category class
class Categories:
    @staticmethod
    def category(data):
        try:
            name = data.get("name")
            description = data.get("description")
            if name:
                name = name.strip()
            if not name or len(name.strip()) < 3:
                return {
                    "error": "Category name must be at least 3 characters long"
                }, HTTP_400_BAD_REQUEST
            if Category.query.filter_by(name=name).first():
                return {"error": "category already exist"}, HTTP_400_BAD_REQUEST
            if not description or len(description) < 10:
                return {
                    "error": "Description must be at least 10 characters long."
                }, HTTP_400_BAD_REQUEST

            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()

            return {"msg": "Category created successfully"}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


# prodct class
class Products:
    @staticmethod
    def products(data):
     try:
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()
        price = data.get("price")
        stock = data.get("stock")
        image_url = data.get("image_url", "").strip()
        category_name = data.get("category_name")

        # Validate name
        if not name or len(name) < 3:
            return {"error": "Product name must be at least 3 characters long."}, HTTP_400_BAD_REQUEST

        # Validate description
        if not description or len(description) < 10:
            return {"error": "Description must be at least 10 characters long."}, HTTP_400_BAD_REQUEST

        # Validate and convert price to float
        try:
            price = float(price)
            if price <= 0:
                return {"error": "Price must be greater than 0."}, HTTP_400_BAD_REQUEST
        except ValueError:
            return {"error": "Price must be a valid number."}, HTTP_400_BAD_REQUEST

        # Validate stock (ensure it's a positive integer)
        if not isinstance(stock, int) or stock < 0:
            return {"error": "Stock must be a non-negative integer."}, HTTP_400_BAD_REQUEST

        # Validate URL (basic check for empty URL)
        if image_url and not image_url.startswith("http"):
            return {"error": "Image URL must be a valid URL starting with http or https."}, HTTP_400_BAD_REQUEST

        # Validate category_id (must be a valid integer)
        if not isinstance(category_name, str):
            return {"error": "Category name must be a string."}, HTTP_400_BAD_REQUEST

        # Create the new product
        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image_url=image_url,
            category_name=category_name
        )

        db.session.add(new_product)
        db.session.commit()

        return {"msg": "Product created successfully"}, HTTP_201_CREATED

     except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR
