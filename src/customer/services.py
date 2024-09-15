from ..model import Customer
from src.constants.Http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ..extensions import db,cache
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_refresh_cookies,
    set_access_cookies,
)
import validators
from datetime import timedelta

from flask import make_response
import logging


logger = logging.getLogger(__name__)


class CustomerServices:
    @staticmethod
    def register(data):
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        city = data.get("city")

        if len(firstname) < 4:
            return {"error": "firstname is too short"}, HTTP_400_BAD_REQUEST
        if len(lastname) < 4:
            return {"error": "lastname is too short!!"}, HTTP_400_BAD_REQUEST
        if len(username) < 4:
            return {"error": "username is too short!!"}, HTTP_400_BAD_REQUEST
        if not validators.email(email):
            return {"error": "email is not valid"}, HTTP_400_BAD_REQUEST
        if Customer.query.filter_by(username=username).first() is not None:
            return {"error": "username already exists"}, HTTP_400_BAD_REQUEST
        if len(password) < 6:
            return {"error": "password is too short"}, HTTP_400_BAD_REQUEST
        if not username.isalnum() or " " in username:
            return {"error": "Username must be alphanumeric"}, HTTP_400_BAD_REQUEST
        if Customer.query.filter_by(email=email).first() is not None:
            return {"error": "email already taken"}, HTTP_400_BAD_REQUEST

        hashed_password = generate_password_hash(password)
        customer = Customer(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            city=city,
            password=hashed_password,
        )
        db.session.add(customer)
        db.session.commit()

        return {"msg": "registration was successful"}, HTTP_200_OK
    

    @staticmethod
    def customer_login(data):
        username = data.get("username")
        password = data.get("password")

        # Create cache key for this customer login
        cache_key = f"customer_{username}"
        logger.debug(f"Cache key: {cache_key}")

        # Check if the result is cached
        cached_res = cache.get(cache_key)
        if cached_res:
            logger.debug(f"Cache res: {cached_res}")
            return cached_res, HTTP_200_OK

        # Query the customer in the database
        customer = Customer.query.filter_by(username=username).first()

        # Check if customer exists and password matches
        if customer and check_password_hash(customer.password, password):
            access_token = create_access_token(identity=customer.id)
            refresh_token = create_refresh_token(identity=customer.id)

            if access_token and refresh_token:
                access_max_age = timedelta(minutes=30)
                refresh_max_age = timedelta(days=30)
                response = make_response({"msg": "successfully login"})

                # Set cookies for access and refresh tokens
                set_access_cookies(response, access_token, max_age=access_max_age)
                set_refresh_cookies(response, refresh_token, max_age=refresh_max_age)

                # Data to cache
                login_data = {
                    "customer": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    }
                }

                # Cache the login data for 5 minutes
                cache.set(cache_key, login_data, timeout=60*5)

                return login_data, HTTP_200_OK

        else:
            logger.debug(f"invalid credentials")
            return {"error": "Invalid login credentials"}, HTTP_400_BAD_REQUEST
