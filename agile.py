import json
import dateutil.parser
import requests
from reel_miami import Config


class AgileSchedule():
    """A class used to represent the schedule for an Agile event."""

    def __init__(self, start_time, buy_link):
        """
        Parameters
        ----------

        start_time : obj
            The showtime for the film as a datetime object.
        buy_link : str
            A link to the direct Agile ticketing page for the given showtime.
        """
        self.start_time = start_time
        self.buy_link = buy_link

    def __repr__(self):
        return f'<Showtime {self.start_time}>'

    def __str__(self):
        return f'{self.start_time}'


class AgileEvent():
    """A class used to represent Agile events, aka films."""

    def __init__(self, name, external_id, duration, showtimes):
        """
        Parameters
        ----------
            name : str
                The name of the event.
            external_id : str
                The external id of the event, used to build the URL to the
                event's page on the organization's website; note that not all
                organizations use the external id in this way.
            duration : str
                The duration of the event.
            showtimes : list
                A collection of instances of Agile Schedule, that is, showtimes
                for the film.
        """

        self.name = name
        self.external_id = external_id
        self.duration = duration
        self.showtimes = showtimes

    def __repr__(self):
        return f'<Film {self.name}>'

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def from_agile_dict(cls, agile_dict):
        """Instantiates both AgileEvent and AgileSchedule using the dictionary
        pulled from the Agile WebSales Feed (JSON-formatted).

        Parameters
        ----------
        agile_dict
            # TODO description

        Returns
        -------
        class
            Instance of class AgileEvent.
        """
        name = agile_dict['Name']
        external_id = agile_dict['ExternalID']
        duration = agile_dict['Duration']
        showtimes = []
        for showing in agile_dict['CurrentShowings']:
            start_time = dateutil.parser.parse(showing['StartDate'])
            buy_link = showing['LegacyPurchaseLink']
            showtimes.append(AgileSchedule(start_time, buy_link))
        return AgileEvent(name, external_id, duration, showtimes)


def build_agile_venue_url(guid, date):
    """Builds a valid URL to access the Agile WebSales Feed for a given venue.

    Paramters
    ---------
    guid: str
        The unique identifier for the Entry Point link in the Agile system.

    Returns
    -------
    str
        A complete URL.
    """
    date = f'&startdate={date}&enddate={date}'
    agile_venue_url = (
                      f'{Config.AGILE_WEBSALES_URL}'
                      f'{guid}'
                      f'{Config.AGILE_PARAMETERS}{date}'
                      )
    return agile_venue_url


def fetch_events(agile_venue_url):
    """Makes a request to the Agile WebSales Feed. Using the returned JSON
    data, the function then instantiates each film and appends it to a list.

    Parameters
    ----------
    date : str
        A date in format YYYY-M-D, e.g. 2019-4-9

    Returns
    -------
    list
        Populated by instances of AgileEvent and sorted by the start time.
    """

    response = requests.get(agile_venue_url)
    feed = json.loads(response.text)
    films = []
    events = feed['ArrayOfShows']
    for event in events:
        film = AgileEvent.from_agile_dict(event)
        films.append(film)

    # Sorts the list of films by their showtimes otherwise they would be
    # displayed alphabetically.
    films.sort(key=lambda film: film.showtimes[0].start_time)

    return films
