import os

from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Feeds
    # Unique identifer for the Entry Point link in the Agile Ticketing system
    CGAC_GUID = os.getenv('CGAC_GUID')  # Coral Gables Art Cinema
    OMB_GUID = os.getenv('OMB_GUID')  # O Cinema Miami Beach

    # Miami Beach Cinematheque RSS feed
    MBC_RSS = os.getenv('MBC_RSS')

    # Tower Theater Miami ticketing URL
    TOWER_TIX = os.getenv('TOWER_TIX')

    # Cosford Cinema base calendar day URL
    COSFORD_TIX = os.getenv('COSFORD_TIX')

    # Flask-Admin
    FLASK_ADMIN_SWATCH = os.getenv('FLASK_ADMIN_SWATCH')
    # Flask-Security
    SECURITY_URL_PREFIX = os.getenv('SECURITY_URL_PREFIX')
    SECURITY_PASSWORD_HASH = os.getenv('SECURITY_PASSWORD_HASH')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = os.getenv('SECURITY_LOGIN_URL')
    SECURITY_LOGOUT_URL = os.getenv('SECURITY_LOGOUT_URL')
    SECURITY_POST_LOGIN_VIEW = os.getenv('SECURITY_POST_LOGIN_VIEW')
    SECURITY_POST_LOGOUT_VIEW = os.getenv('SECURITY_POST_LOGOUT_VIEW')

    # Flask-Security features
    SECURITY_REGISTER_EMAIL = os.getenv('SECURITY_REGISTER_EMAIL')

    # Heroku
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
