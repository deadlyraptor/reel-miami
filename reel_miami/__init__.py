# __init__.py

from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from reel_miami.main.routes import main
    from reel_miami.utils.filters import filters
    app.register_blueprint(main)
    app.register_blueprint(filters)

    return app
