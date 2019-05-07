from datetime import datetime, timezone
import feedparser
from config import Config


class MBCEvent():
    """A class used to represent MBC events, aka films."""

    def __init__(self, name, info_link, showtimes):
        """
        Parameters
        ----------
        name : str
            The name of the event.
        info_link : str
            The link to the event page on the MBC website.
        showtimes : object
            A class with showtime info.
        """
        self.name = name
        self.info_link = info_link
        self.showtimes = showtimes

    def __repr__(self):
        return f'<Film {self.name}>'

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def rename(cls, title):
        """Strips the title of the event from the title element in the RSS feed

        Parameters
        ----------
        title : str
            The raw title, e.g.
            Miami Theatrical Premiere! THE ROOM by Tommy Wiseau

        Returns
        -------
        str
            The title of the film (title cased) without the extraneous
            information.

        """

        split_on_exclamation = title.split('! ')
        name = split_on_exclamation[1].split(' by')[0].title()
        return name

    @classmethod
    def from_mbc_feed(cls, event):
        """Instatiates both MBCEvent and MBCSchedule using the RSS feed
        supplied by the MBC website.

        Parameters
        ----------
        event : object
            # TODO description

        Returns
        -------
        object
            An instance of class MBCEvent.

        """
        name = MBCEvent.rename(event.title)
        info_link = event.link
        show_date = MBCSchedule.parse_show_date(event)
        start_time = MBCSchedule.parse_start_time(event)
        buy_link = event.link
        showtime = MBCSchedule(show_date, start_time, buy_link)

        return MBCEvent(name, info_link, showtime)


class MBCSchedule():
    """A class used to represent the schedule for an MBC event."""

    def __init__(self, date, start_time, buy_link):
        """
        Parameters
        ----------
        date : str
            The date of the showtime, formatted %Y-%m-%d,
        start_time : str
            The showtime, formatted %I:%M%p.
        buy_link : str
            The link to the ticketing page on the MBC website.
        """
        self.date = date
        self.start_time = start_time
        self.buy_link = buy_link

    def __repr__(self):
        return f'<Showtime {self.date} {self.start_time}>'

    def __str__(self):
        return f'{self.date} (self.start_time)'

    @classmethod
    def parse_show_date(cls, event):
        showtime = datetime.strptime(event.published,
                                     '%a, %d %b %Y %H:%M:%S %Z')
        local_time = gmt_to_local(showtime)
        show_date = local_time.strftime('%Y-%m-%d')

        return show_date

    @classmethod
    def parse_start_time(cls, event):
        showtime = datetime.strptime(event.published,
                                     '%a, %d %b %Y %H:%M:%S %Z')
        local_time = gmt_to_local(showtime)
        start_time = local_time.strftime('%I:%M%p').lower().lstrip('0')

        return start_time


def gmt_to_local(gmt_datetime):
    """Converts the GMT date & time from the RSS feed into local (UTC) time.

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


def fetch_mbc_events(date):
    """Creates a feedparser object from the MBC RSS feed that is used to create
    a list of films (instances of MBCEvent and MBCSchedule).

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
        parsed_date = datetime.strptime(showtime, '%a, %d %b %Y %H:%M:%S %Z')
        est = gmt_to_local(parsed_date)
        if est.strftime('%Y-%m-%d') == date:
            film = MBCEvent.from_mbc_feed(event)
            films.append(film)

    return films
