from flask import Blueprint,jsonify
from src.constants.Http_status_code import HTTP_500_INTERNAL_SERVER_ERROR
from flask_jwt_extended import jwt_required
from .controllers import list_of_product

product_bp = Blueprint("product", __name__, url_prefix="/api/v1/product")

# product list
@product_bp.get("/product_list")
def all_product():
    try:
        response,status_code= list_of_product()
        return jsonify(response),status_code
    except Exception as e:
        return {"error":str(e)}, HTTP_500_INTERNAL_SERVER_ERROR 