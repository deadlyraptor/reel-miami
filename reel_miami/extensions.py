from flask_admin import Admin
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

admin = Admin(name='Admin', base_template='admin_master.html',
              template_mode='bootstrap3')
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
