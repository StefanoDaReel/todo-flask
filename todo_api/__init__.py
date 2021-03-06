from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.url_map.strict_slashes = False

    db.init_app(app)
    ma.init_app(app)

    from .urls import bp
    app.register_blueprint(bp)

    return app
