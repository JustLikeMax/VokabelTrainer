import logging
import os
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

logger = logging.getLogger(__name__)

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app() -> Flask:
    app = Flask(__name__)
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        secret_key = secrets.token_hex(32)
        logger.warning(
            "SECRET_KEY is not set. A random key has been generated; "
            "sessions and CSRF tokens will be invalidated on restart. "
            "Set the SECRET_KEY environment variable for production use."
        )
    app.secret_key = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vokabeln.db"

    db.init_app(app)
    csrf.init_app(app)

    from .routes import register_routes

    register_routes(app)

    return app
