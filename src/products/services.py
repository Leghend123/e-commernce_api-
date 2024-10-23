from ..extensions import db
from ..model import Product, User
from ..constants.Http_status_code import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)
from flask_jwt_extended import get_jwt_identity


class Products:
    @staticmethod
    def list_of_all_product():
        try:
            _products = Product.query.all()
            data = []
            for product in _products:
                data.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "price": f"${product.price}",
                        "stock": product.stock,
                        "category_name": product.category_name,
                    }
                )
            return {"data": data}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def add_stock(data):
        try:
            current_user = get_jwt_identity()

            # Check if the user exists and if they are an admin
            user = User.query.filter_by(id=current_user).first()
            if not user:
                return {"error": "User not found"}, HTTP_404_NOT_FOUND
        
            if not user.is_admin:
                return {"error": "Only admins can add to stock"}, HTTP_403_FORBIDDEN
        
            # Check if product_id and quantity are provided in the request
            product_id = data.get("product_id")
            quantity = data.get("quantity")

            if not product_id or quantity is None:
                return {"error": "product_id or quantity not provided"}, HTTP_400_BAD_REQUEST
        
            # Query the product
            product = Product.query.filter_by(id=product_id).first()
            if not product:
                return {"error": "Product not found"}, HTTP_404_NOT_FOUND

            # Update the stock
            product.stock += quantity
            db.session.commit()

            return {"message": "Stock updated successfully"}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR

