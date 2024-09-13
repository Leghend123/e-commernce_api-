from ..model import Customer
from src.constants.Http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import validators
from flask import jsonify, request


class CustomerServices:
    @staticmethod
    def register(data):
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        city = data.get('city')

        if len(firstname) < 4:
            return {"error": "firstname is too short"}, HTTP_400_BAD_REQUEST
        if len(lastname) < 4:
            return {"error": "lastname is too short!!"}, HTTP_400_BAD_REQUEST
        if len(username) < 4:
            return {"error": "username is too short!!"}, HTTP_400_BAD_REQUEST
        if not validators.email(email):
            return {"error": "email is not valid"}, HTTP_400_BAD_REQUEST
        if Customer.query.filter_by(username=username).first() is not None:
            return {"error": "username already exist"}, HTTP_400_BAD_REQUEST
        if len(password) < 6:
            return {"error": "password is too short"}, HTTP_400_BAD_REQUEST
        if not username.isalnum() or " " in username:
            return {"error": "Username must be alphanumeric"}, HTTP_400_BAD_REQUEST
        if Customer.query.filter_by(email=email).first() is not None:
            return {"error": "email already taken"}, HTTP_400_BAD_REQUEST

        hashed_password = generate_password_hash(password)
        customer = Customer(
            firstname=firstname, lastname=lastname, username=username, email=email, city=city, password=hashed_password)
        db.session.add(customer)
        db.session.commit()

        return {"msg": "registration was successfully"}, HTTP_200_OK
    
    @staticmethod
    def customer_login(data):
        username= data.get('username')

