# __init__.py

from flask import Flask
from flask_admin import Admin
from flask_admin.base import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='Reel Miami', template_mode='bootstrap3')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from reel_miami import models

    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    admin.add_view(models.AdminVenue(models.Venue, db.session, 'Venues'))
    admin.add_link(MenuLink(name='Public Website', url=('/')))

    from reel_miami.main.routes import main
    from reel_miami.utils.filters import filters
    from reel_miami.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(filters)
    app.register_blueprint(errors)

    return app
