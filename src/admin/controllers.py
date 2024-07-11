from flask import request, jsonify
from .services import UserService
from src.constants.Http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


def add_admin():
    try:
        data = request.get_json()
        response, status_code = UserService.add_admin(data)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def login():
    try:
        data = request.get_json()
        response, status_code = UserService.login(data)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def refresh_user_token():
    try:
        response, status_code = UserService.refresh_user_token()
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def current_admin():
    try:
        response, status_code = UserService.current_admin()
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def get_all_admin():
    try:
        response, status_code = UserService.get_all_admin()
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def get_admin_by_id(id):
    try:
        response, status_code = UserService.get_admin_by_id(id)
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


def logout():
    try:
        response, status_code = UserService.logout()
        return response, status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR
