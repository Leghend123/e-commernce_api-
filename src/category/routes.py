from flask import Blueprint, jsonify
from ..constants.Http_status_code import HTTP_500_INTERNAL_SERVER_ERROR
from .controllers import category_list


category_bp = Blueprint("category", __name__, url_prefix="/api/v1/category")

#category route
@category_bp.get("/category_list")
def list_of_category():
    try:
        response, status_code = category_list()
        return jsonify(response), status_code
    except Exception as e:
        return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR
