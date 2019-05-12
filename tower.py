from datetime import datetime
import requests
from bs4 import BeautifulSoup
from config import Config


class TowerFilm():
    """A class used to represent Tower Theater events, aka films."""

    def __init__(self, name, showtimes):
        """
        Parameters
        ----------
        name : str
            The name of the event.
        showtimes : list
            A collection of instances of TowerSchedule, that is, showtimes for
            the film.
        """
        self.name = name
        self.showtimes = showtimes

    def __repr__(self):
        return f'<Film {self.name}>'

    def __str__(self):
        return f'{self.name}'


class TowerSchedule():
    """A class used to represent the schedeule for a Tower Theater events."""

    def __init__(self, date, start_time, buy_link):
        """
        Parameters
        ----------
        date : str
            The playdate for the event.
        start_time : str
            The showtime for the event.
        buy_link : str
            A link to the direct Veezie ticketing page for the given showtime.
        """
        self.date = date
        self.start_time = start_time
        self.buy_link = buy_link

    def __repr__(self):
        return f'<Showtime {self.date} {self.start_time}>'

    def __str__(self):
        return f'{self.date} {self.start_time}'


def fetch_tower_events(today):
    """Fetchs the HTML document from Tower Theater's Veezie ticketing page. The
    parameter is used to focus on a specific date as the HTML document contains
    the full schedule for the venue, including multiple dates of screenings.

    Parameters
    ----------
    today : str
        A date in the format YYYY-M-D.

    Returns
    -------
    list
        A collection of instances of TowerFilm.
    """

    r = requests.get(Config.TOWER_TIX)
    soup = BeautifulSoup(r.text, 'html.parser')

    # The date passed in by the route is in a format different from the date
    # string in the HTML document so the desired date has to reformatted to
    # match the HTML document's version.
    new_today = datetime.strptime(today, '%Y-%m-%d').strftime('%A %-d, %B')

    films = []
    # get all the dates in the document in order to find the desired one
    dates = soup.find_all('h3', 'date-title')
    for date in dates:
        # find the div tag that matches the given date
        if new_today == date.get_text():
            # date_soup points to the div (and corresponding child elements)
            # for all films showing on the given date so we only parse a
            # smaller section of the HTML document.
            date_soup = date.parent
            # film_tags is a list containing every div that contains film info
            film_tags = date_soup.find_all('div', class_='film')
            # we loop over each individual film div
            for film_tag in film_tags:
                # this gets the name of the film
                name_tags = film_tag.find_all('h3', class_='title')
                for name_tag in name_tags:
                    name = name_tag.get_text().strip()

                # this gets the playdate of the film
                # possibly unneccessary because the date is passed in earlier
                playdate_tags = film_tag.find_all('h4', class_='date')
                for playdate_tag in playdate_tags:
                    playdate = playdate_tag.get_text()

                # this gets the showtimes and corresponding ticketing links
                sessions = film_tag.find('ul', class_='session-times')
                li_tags = sessions.find_all('li')
                showtimes = []
                for li_tag in li_tags:
                    start_time = li_tag.a.time.get_text()
                    buy_link = li_tag.a['href']
                    # for every showtime, create an instance of TowerSchedule
                    showtime = TowerSchedule(playdate, start_time, buy_link)
                    showtimes.append(showtime)
                # create a new instance of TowerFilm during every loop of the
                # film divs
                film = TowerFilm(name, showtimes)
                films.append(film)

    return films
