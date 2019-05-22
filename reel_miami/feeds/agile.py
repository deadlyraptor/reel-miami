from dataclasses import dataclass
import dateutil.parser
import requests
from .film import FilmEvent, FilmSchedule


@dataclass
class AgileEvent(FilmEvent):
    """A subclass used for methods specific to Agile Ticketing venues.

    Parameters
    ----------
    duration : str
        The duration of the event.

        This defaults to None because the last parameter in the parent class
        defaults to None.

    """

    duration: str = None

    def from_agile_dict(event):
        """Instantiate both AgileEvent and AgileSchedule.

        The class parameters are pulled from a dictionary provided by the
        Agile WebSales Feed (JSON format).

        Parameters
        ----------
        event
            A dictionary (JSON) containing the info for an event in the Agile
            WebSales Feed.

            It includes a subdictionary called CurrentShowings that contains
            the showtimes for the event.

        Returns
        -------
        AgileEvent
            Instance of class AgileEvent.

        """
        name = event['Name']
        film_link = event['InfoLink']
        duration = event['Duration']
        showtimes = []
        for showing in event['CurrentShowings']:
            start_time = dateutil.parser.parse(showing['StartDate'])
            ticketing_link = showing['LegacyPurchaseLink']
            showtimes.append(FilmSchedule(start_time, ticketing_link))

        return AgileEvent(name, showtimes, film_link, duration)

    def fetch_agile_events(guid, date):
        """Make a request to the Agile WebSales Feed and build a list of films.

        Parameters
        ----------
        guid : str
            The unique identifier for the Entry Point link in the Agile system.
            This determines which venue to poll (CGAC or OMB).
        date : str
            The date for which to pull showtimes.

        Returns
        -------
        films
            A list populated by instances of AgileEvent.

            The list is sorted by the showtimes otherwise they would be listed
            alphabetically.

        """

        payload = {'guid': guid, 'showslist': 'true', 'format': 'json',
                   'startdate': date, 'enddate': date}
        base_agile_url = 'https://prod3.agileticketing.net/websales/feed.ashx?'

        response = requests.get(base_agile_url, params=payload)
        feed = response.json()
        films = []
        # the feed returns a truncated dictionary if the venue has no events so
        # this conditional statement checks that the required data exists
        if len(feed) == 3:
            pass
        else:
            events = feed['ArrayOfShows']
            for event in events:
                film = AgileEvent.from_agile_dict(event)
                films.append(film)

        films.sort(key=lambda film: film.showtimes[0].start_time)

        return films
