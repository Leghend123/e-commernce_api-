from .services import OrderServices
from src.constants.Http_status_code import HTTP_500_INTERNAL_SERVER_ERROR
from flask import request

def list_of_orders():
    try:
        response, status_code = OrderServices.order_list()
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def order_detials():
    try:
        data = request.get_json()
        response, status_code = OrderServices.order_details(data)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR
