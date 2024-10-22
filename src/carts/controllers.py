from .services import CartServices
from src.constants.Http_status_code import HTTP_500_INTERNAL_SERVER_ERROR
from flask import request
from flask_jwt_extended import get_jwt_identity


def add_to_guest():
    try:
        data = request.get_json()
        response, status_code = CartServices.add_to_guest_cart(data)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def view_cart():
    try:
        response, status_code = CartServices.view_guest_cart()
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def save_cart_on_login():
    try:
        customer_id = get_jwt_identity()
        response, status_code = CartServices.save_to_cart_db(customer_id)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def load_cart():
    try:
        customer_id = get_jwt_identity()
        response, status_code = CartServices.load_saved_cart(customer_id)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def remove_cart_items():
    try:
        data = request.get_json()
        response, status_code = CartServices.reomve_item_cart(data)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def checkout():
    try:
        customer_id = get_jwt_identity()
        response, status_code = CartServices.checkout(customer_id)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

def updated_cart():
    try:
        data = request.get_json()
        response, status_code = CartServices.update_quantity_of_items(data)
        return response , status_code
    except Exception as e:
        return {"error":str(e)}, HTTP_500_INTERNAL_SERVER_ERROR