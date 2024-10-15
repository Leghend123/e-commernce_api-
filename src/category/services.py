from ..extensions import db
from ..model import Category
from src.constants.Http_status_code import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)


class Categories:
    @staticmethod
    def category_list():
        try:
            categories = Category.query.all()
            data = []
            for category in categories:
                data.append(
                    {
                        "id": category.id,
                        "name": category.name,
                        "description": category.description,
                        "created_at": category.created_at,
                    }
                )
            return {"data": data}, HTTP_200_OK

        except Exception as e:
            return {"error": str(e)}, HTTP_500_INTERNAL_SERVER_ERROR
