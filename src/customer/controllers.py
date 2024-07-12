from flask import request
from .services import CustomerServices
from src.constants.Http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


def register():
    try:
        data = request.get_json()
        response, status_code = CustomerServices.register(data)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR
