# __init__.py

from flask import Flask, url_for
from flask_admin import helpers as admin_helpers
from flask_admin.base import MenuLink
from flask_security import Security, SQLAlchemyUserDatastore

from reel_miami.extensions import admin, db, mail, migrate
from reel_miami.errors.handlers import errors
from reel_miami.main.routes import main
from reel_miami.utils.filters import filters

from settings import Config
from reel_miami import models


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)
    register_blueprints(app)

    user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
    security = Security(app, user_datastore)

    admin.add_view(models.AdminVenueView(models.Venue, db.session, 'Venues'))
    admin.add_view(models.AdminRoleView(models.Role, db.session, 'Roles'))
    admin.add_view(models.AdminUserView(models.User, db.session, 'Users'))
    admin.add_link(MenuLink(name='Reel Miami', url=('/')))

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
            )

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main)
    app.register_blueprint(filters)
    app.register_blueprint(errors)

    return None
