from .services import Categories
from src.constants.Http_status_code import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
)


def category_list():
    try:
        response,status_code=Categories.category_list()
        return response,status_code
    except Exception as e:
        return{"error":str(e)},HTTP_500_INTERNAL_SERVER_ERROR
