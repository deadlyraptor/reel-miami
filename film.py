from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class FilmSchedule:
    """A class used to represent the schedule for a film event.

    Parameters
    ----------
    start_time : datetime
        The showtime for the screening.
    ticketing_link : str
        The URL to the screening's ticketing page.
    """

    start_time: datetime
    ticketing_link: str

    def __str__(self):
        return f'{self.play_date} {self.start_time}'


@dataclass
class FilmEvent:
    """A class used to represent film events.

    Parameters
    ----------
    name : str
        The name of the event.
    showtimes : list
        A collection of instances of FilmSchedule.
    film_link : str
        The URL to the film's info page.
    """

    name: str
    showtimes: List[FilmSchedule]
    film_link: str = None

    def __str__(self):
        return f'{self.name}'
