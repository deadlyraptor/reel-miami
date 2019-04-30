# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from reel_miami import models

    db.init_app(app)
    migrate.init_app(app, db)

    from reel_miami.main.routes import main
    from reel_miami.utils.filters import filters
    app.register_blueprint(main)
    app.register_blueprint(filters)

    return app
