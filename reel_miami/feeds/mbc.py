from dataclasses import dataclass
from datetime import datetime, timezone

import feedparser
from flask import current_app

from .film import FilmEvent, FilmSchedule


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

            MBC events are titled in several ways. The conditional blocks
            check for each of them and formats the string accordingly.

        Returns
        -------
        name
            The title of the film (title cased) as a string.

        """
        if title.startswith('"'):
            # "BAD MOVIES 101" A Series: THE ROOM by Tommy Wiseau
            name = title.split(': ')[1].split(' by')[0].title()
        elif '! ' in title:
            # Miami Theatrical Premiere! THE ROOM by Tommy Wiseau
            # Miami Theatrical Premiere! THE ROOM
            name = title.split('! ')[1].split(' by')[0].title()
            if '(' in name:
                # Miami Theatrical Premiere! THE ROOM (11 January 1900)
                name = title.split(' (')[0].split('! ')[1].title()
        elif '(' in title:
            # BAD MOVIE NIGHT: A series of horrible films
            name = title.split(' (')[0]
        else:
            # Just use the title as is
            name = title

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
        """Instatiate both MBCEvent and MBCSchedule using MBC RSS feed.

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
        showtimes = []
        start_time = MBCSchedule.parse_start_time(event)
        ticketing_link = event.link
        showtime = MBCSchedule(start_time, ticketing_link)
        showtimes.append(showtime)

        return MBCEvent(name, showtimes, film_link)

    def fetch_mbc_events(date):
        """Create a feedparser object from the MBC RSS feed.

        This object is used to create a list of films (instances of MBCEvent
        and MBCSchedule).

        Parameters
        ----------
        date : str
            The date for which we want to gather showtimes.

        Returns
        -------
        list
            Populated by instances of MBCEvent and MBCSchedule.

        """
        feed = feedparser.parse(current_app.config['MBC_RSS'])
        films = []
        events = feed.entries
        temp_films = []

        for event in events:
            if event.title not in temp_films:
                temp_films.append(event.title)
                # this ensures we only work with the chosen date's events
                showtime = event.published
                parsed_date = datetime.strptime(showtime,
                                                '%a, %d %b %Y %H:%M:%S %Z')
                est = MBCEvent.gmt_to_local(parsed_date)
                if est.strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d'):
                    film = MBCEvent.from_mbc_feed(event)
                    films.append(film)
            elif event.title in temp_films:
                # this ensures we only work with the chosen date's events
                showtime = event.published
                parsed_date = datetime.strptime(showtime,
                                                '%a, %d %b %Y %H:%M:%S %Z')
                est = MBCEvent.gmt_to_local(parsed_date)
                if est.strftime('%Y-%m-%d') == date.strftime('%Y-%m-%d'):
                    start_time = MBCSchedule.parse_start_time(event)
                    ticketing_link = event.link
                    showtime = MBCSchedule(start_time, ticketing_link)
                    for film in films:
                        if MBCEvent.rename(event.title) == film.name:
                            film.showtimes.append(showtime)

        return films
