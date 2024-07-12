from ..model import Customer
from src.constants.Http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import validators


class CustomerServices:
    @staticmethod
    def register():
        pass
