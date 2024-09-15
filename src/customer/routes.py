from flask import Blueprint, jsonify
from .controllers import register, customer_login
from flask_jwt_extended import jwt_required
from src.constants.Http_status_code import HTTP_500_INTERNAL_SERVER_ERROR


customer = Blueprint('customer', __name__, url_prefix='/api/v1/customer')


@customer.post('/register')
# @jwt_required()
def register_customer():
    try:
        response, status_code = register()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

@customer.post('/customer_login')
def login():
    try:
        response,status_code = customer_login()
        return jsonify(response),status_code
    except Exception as e:
        return jsonify({"error":str(e)}), HTTP_500_INTERNAL_SERVER_ERROR