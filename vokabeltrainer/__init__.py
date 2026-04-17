from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vokabeln.db"

    db.init_app(app)

    from .routes import register_routes

    register_routes(app)

    return app
