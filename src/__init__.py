from flask import Flask
from src.admin.routes import admin_bp
from src.customer.routes import customer
import os
from src.extensions import db
from flask_jwt_extended import JWTManager
from src.admin.services import UserService


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            # JWT_ACCESS_COOKIE_PATH='/',
            # JWT_REFRESH_COOKIE_PATH='/token/refresh'
        )
    else:
        app.config.from_mapping(test_config)

    # app.register_blueprint(auth)
    app.register_blueprint(admin_bp)
    app.register_blueprint(customer)
    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()
        UserService.default_admin()

    return app
