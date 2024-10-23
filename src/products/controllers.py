from flask import request
from .services import Products
from src.constants.Http_status_code import HTTP_500_INTERNAL_SERVER_ERROR


def list_of_product():
    try:
        response, status_code = Products.list_of_all_product()
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

def add_stocks():
    try:
        data = request.get_json()
        response,status_code = Products.add_stock(data)
        return response, status_code
    except Exception as e:
        return {"error":str(e)}, HTTP_500_INTERNAL_SERVER_ERROR