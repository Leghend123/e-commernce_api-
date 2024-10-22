from flask import Blueprint, jsonify
from src.constants.Http_status_code import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from .controllers import (
    add_to_guest,
    view_cart,
    save_cart_on_login,
    load_cart,
    checkout,
    remove_cart_items,
    updated_cart,
)
from flask_jwt_extended import jwt_required


cart_bp = Blueprint("cart", __name__, url_prefix="/api/v1/carts")


@cart_bp.post("/add_cart")
def cart():
    try:
        response, status_code = add_to_guest()
        return jsonify(response), status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


@cart_bp.get("/view_cart")
def view_your_cart():
    try:
        response, status_code = view_cart()
        return jsonify(response), status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


@cart_bp.post("/save_cart")
@jwt_required()
def saveCart():
    try:
        response, status_code = save_cart_on_login()
        return jsonify(response), status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


@cart_bp.get("/load_cart")
@jwt_required()
def load_cart_data_from_db():
    try:
        response, status_code = load_cart()
        return jsonify(response), status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


@cart_bp.post("/checkout")
@jwt_required()
def cart_checkout():
    try:
        response, stats_code = checkout()
        return jsonify(response), stats_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


@cart_bp.post("/remove_item")
def removeItems():
    try:
        response, status_code = remove_cart_items()
        return jsonify(response), status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR


@cart_bp.post("/quantity_update")
def quantityUpdate():
    try:
        response, status_code = updated_cart()
        return jsonify(response), status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR
