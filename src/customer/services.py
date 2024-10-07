from ..model import Customer
from src.constants.Http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST
from ..extensions import db, cache, mail
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_refresh_cookies,
    set_access_cookies,
    decode_token,
)
import validators
from datetime import timedelta, datetime, timezone
from flask import make_response, url_for, request
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
                cache.set(cache_key, login_data, timeout=60 * 5)

                return login_data, HTTP_200_OK

        else:
            logger.debug(f"invalid credentials")
            return {"error": "Invalid login credentials"}, HTTP_400_BAD_REQUEST

    @staticmethod
    def forgot_password(data):
        email = data.get("email")

        customer = Customer.query.filter_by(email=email).first()

        if not customer:
            return {
                "error": "no account associated with this email"
            }, HTTP_400_BAD_REQUEST

        # generate access token
        reset_token = create_access_token(
            identity=customer.id, expires_delta=timedelta(minutes=20)
        )

        # generate reset url
        reset_url = url_for(
            "customer.password_reset_confrim", token=reset_token, _external=True
        )

        try:
            send_mail.send_reset_email(customer.email, reset_url)
            logger.debug(f"customer_email{email}")

        except Exception as e:
            return {"error": "Failed to send email"}, HTTP_400_BAD_REQUEST

        return {
            "message": {
                "msg": "Reset email has been sent successfully",
                "reset_token": reset_token,
                "reset_url": reset_url
            }
        }, HTTP_200_OK

    @staticmethod
    def update_password(token, data):
        try:
            decoded_token = decode_token(token)
            customer_id = decoded_token["sub"]

            new_password = data.get("password")
            if not new_password or len(new_password) < 6:
                return {"error": "password too short"}, HTTP_400_BAD_REQUEST

            customer = Customer.query.get(customer_id)
            if not customer:
                return {"error": "customer not found"}, HTTP_400_BAD_REQUEST

            customer.password = generate_password_hash(new_password)
            db.session.commit()

            return {"message": "password has been updated succesfully!"}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_400_BAD_REQUEST


# class for sending the mail
class send_mail:
    @staticmethod
    def send_reset_email(email, reset_url):
        sender = "nelsonagbagah1002@gmail.com"
        subject = "Password Reset Request"
        body = f"To reset your password, click the following link: {reset_url}\nIf you did not make this request, please ignore this email."

        # Create a message object
        msg = Message(subject, sender=sender, recipients=[email])
        msg.body = body

        # Send email
        try:
            mail.send(msg)
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise e
