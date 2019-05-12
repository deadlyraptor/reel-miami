import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        f'sqlite:///{os.path.join(basedir, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # The base URL for ticketing data from Agile.
    # Will not work without a guid.
    AGILE_WEBSALES_URL = os.environ.get('AGILE_WEBSALES_URL')

    # Returns the WebSales data as Shows with Showings grouped underneath and
    # in JSON format
    AGILE_PARAMETERS = os.environ.get('AGILE_PARAMETERS')

    # Unique identifer for the Entry Point link in the Agile system
    CGAC_GUID = os.environ.get('CGAC_GUID')  # Coral Gables Art Cinema
    OMB_GUID = os.environ.get('OMB_GUID')  # O Cinema Miami Beach

    # Miami Beach Cinematheque RSS feed
    MBC_RSS = os.environ.get('MBC_RSS')

    # Tower Theater Miami ticketing URL
    TOWER_TIX = os.environ.get('TOWER_TIX')
