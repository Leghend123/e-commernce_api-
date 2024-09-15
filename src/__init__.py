import logging.config
import os
from flask import Flask
from flask_caching import Cache
from src.admin.routes import admin_bp
from src.customer.routes import customer
from src.extensions import db,cache
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.admin.services import UserService

# Initialize global Cache


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # Configure Flask-Caching to use Redis
    app.config["CACHE_TYPE"] = "redis"
    app.config["CACHE_REDIS_HOST"] = "localhost"
    app.config["CACHE_REDIS_PORT"] = 6379
    app.config["CACHE_REDIS_DB"] = 0
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # Cache timeout of 5 minutes

    # Initialize cache
    cache.init_app(app)

    # logging configuration
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s %(name)s %(levelname)s: %(message)s",
            },
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "maxBytes": 100000,
                "backupCount": 4,
                "level": "DEBUG",
                "formatter": "detailed",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["file"],
        },
    }

    # Configure app settings
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    else:
        app.config.from_mapping(test_config)

    # Configure Flask-Caching to use Redis
    # app.config["CACHE_TYPE"] = "RedisCache"
    # app.config["CACHE_REDIS_HOST"] = "localhost"
    # app.config["CACHE_REDIS_PORT"] = 6379
    # app.config["CACHE_REDIS_DB"] = 0
    # app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
    # app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # Cache timeout of 5 minutes

    # Apply the logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)

    # Register blueprints and extensions
    app.register_blueprint(admin_bp)
    app.register_blueprint(customer)

    db.init_app(app)
    # Initialize cache
    cache.init_app(app)
    JWTManager(app)
    CORS(app)

    with app.app_context():
        db.create_all()
        UserService.default_admin()

    return app
