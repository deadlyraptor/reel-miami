# __init__.py

from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
migrate = Migrate()
admin = Admin()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from reel_miami import models

    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    admin.add_view(models.AdminVenue(models.Venue, db.session, 'Venues'))

    from reel_miami.main.routes import main
    from reel_miami.utils.filters import filters
    from reel_miami.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(filters)
    app.register_blueprint(errors)

    return app
