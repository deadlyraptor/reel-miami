from dataclasses import dataclass
from datetime import datetime, timezone
import feedparser
from .film import FilmEvent, FilmSchedule
from config import Config


@dataclass
class MBCSchedule(FilmSchedule):
    """A subclass used for methods specific to the MBC RSS feed schedule."""

    def parse_start_time(event):
        showtime = datetime.strptime(event.published,
                                     '%a, %d %b %Y %H:%M:%S %Z')
        start_time = MBCEvent.gmt_to_local(showtime)

        return start_time


@dataclass
class MBCEvent(FilmEvent):
    """A subclass used for methods specific to the MBC RSS feed."""

    def rename(title):
        """Strip the title of the event from the title element in the RSS feed.

        Parameters
        ----------
        title : str
            The raw title from the RSS feed.

            MBC events are titled in one of two ways. The conditional block
            accounts for both formats and splits the text accordingly.

            Examples titles:
            Miami Theatrical Premiere! THE ROOM by Tommy Wiseau
            "BAD MOVIES 101" A series: THE ROOM by Tommy Wiseau

        Returns
        -------
        name
            The title of the film (title cased) as a string.

        """
        if title.startswith('"'):
            name = title.split(': ')[1].split(' by')[0].title()
        else:
            name = title.split('! ')[1].split(' by')[0].title()

        return name

    def gmt_to_local(gmt_datetime):
        """Convert GMT date & time from the RSS feed into local (UTC) time.

        Parameters
        ----------
        gmt_datetime : str
            The date and time of the event in GMT timezone.

        Returns
        -------
        datetime
            The date and time of the event in 24-hour EST time.

        """
        local_time = gmt_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)

        return local_time

    def from_mbc_feed(event):
        """Instatiates both MBCEvent and MBCSchedule using the RSS feed
        supplied by the MBC website.

        Parameters
        ----------
        event : object
            The feedparser class that contains the RSS data for a single event.

        Returns
        -------
        MBCEvent
            An instance of class MBCEvent.

        """
        name = MBCEvent.rename(event.title)
        film_link = event.link
        start_time = MBCSchedule.parse_start_time(event)
        ticketing_link = event.link
        showtime = MBCSchedule(start_time, ticketing_link)

        return MBCEvent(name, showtime, film_link)

    def fetch_mbc_events(date):
        """Creates a feedparser object from the MBC RSS feed that is used to
        create a list of films (instances of MBCEvent and MBCSchedule).

        Parameters
        ----------
        date : str
            The date for which we want to gather showtimes.

        Returns
        -------
        list
            Populated by instances of MBCEvent and MBCSchedule.
        """

        feed = feedparser.parse(Config.MBC_RSS)
        films = []
        events = feed.entries
        for event in events:
            # this ensures we only work with the chosen date's events
            showtime = event.published
            parsed_date = datetime.strptime(showtime,
                                            '%a, %d %b %Y %H:%M:%S %Z')
            est = MBCEvent.gmt_to_local(parsed_date)
            if est.strftime('%Y-%m-%d') == date:
                film = MBCEvent.from_mbc_feed(event)
                films.append(film)

        return films
