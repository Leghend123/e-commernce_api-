from ..extensions import db
from ..model import Product
from ..constants.Http_status_code import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)


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
                        "price": product.price,
                        "stock": product.stock,
                        "category_name": product.category_name
                    }
                )
            return {"data": data}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR
