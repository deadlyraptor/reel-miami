import os


class Config():
    # The base URL for ticketing data from Agile.
    # Will not work without a guid.
    AGILE_WEBSALES_URL = os.environ.get('AGILE_WEBSALES_URL')

    # Returns the WebSales data as Shows with Showings grouped underneath and
    # in JSON format
    AGILE_PARAMETERS = os.environ.get('AGILE_PARAMETERS')

    # Unique identifer for the Entry Point link in the Agile system
    CGAC_GUID = os.environ.get('CGAC_GUID')  # Coral Gables Art Cinema
    OMB_GUID = os.environ.get('OMB_GUID')  # O Cinema Miami Beach
