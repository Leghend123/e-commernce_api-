from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from .controllers import list_of_orders, order_detials
from src.constants.Http_status_code import HTTP_500_INTERNAL_SERVER_ERROR


order_bp = Blueprint("order", __name__, url_prefix="/api/v1/order")


@order_bp.get("/orders")
@jwt_required()
def my_orders():
    try:
        response, status_code = list_of_orders()
        return jsonify(response), status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


@order_bp.post("/view_order_details")
@jwt_required()
def view_detials():
    try:
        response, status_code = order_detials()
        return jsonify(response), status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR
