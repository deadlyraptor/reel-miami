from bs4 import BeautifulSoup
import dateutil.parser
from flask import current_app
import requests

from .film import FilmEvent, FilmSchedule


def fetch_cosford_events(date):
    """Fetch the HTML document for the Cosford Cinema website.

    Parameters
    ----------
    date : str
        The date to search for.

    Returns
    -------
    films
        A collection of instances of FilmEvent.

    """
    r = requests.get(f'{current_app.config["COSFORD_TIX"]}{date}')
    soup = BeautifulSoup(r.text, 'html.parser')

    films = []

    # film_soup points to a list containing every div with screening info
    film_soup = soup.find_all('div', class_='views-field-title')
    # keeps track of all films so multiple instances of the same film
    # aren't instantiated
    temp_films = []
    for film_tag in film_soup:
        name = film_tag.get_text().strip()
        showtimes = []
        if name not in temp_films:  # if the film isn't in our temporary list
            temp_films.append(name)  # add the film to the list

            # the following four lines instantiate FilmSchedule just like every
            # other feed script. the class is instantiated in the first pass
            # otherwise the first showtime would never be added
            film_link = (f'http://www.cosfordcinema.com'
                         f'{film_tag.find_all("a", string=name)[0]["href"]}')
            start_time = film_tag.findNext('div').get_text().strip()
            showtimes.append(FilmSchedule(dateutil.parser.parse(start_time),
                                          film_link))

            # the following two lines instantiate FilmEvent just like every
            # other feed script. the name is title cased here because we need
            # it in the original UPPER CASE in order to pass it as the string
            # used to find the corresponding link tag
            film = FilmEvent(name.title(), showtimes, film_link)
            films.append(film)

        # if the film is already in the temporary list, then we just grab the
        # corresponding showtime, instantiate FilmSchedule accordingly, and
        # then append this new instance to the showtimes list that exists in
        # the appropriate FilmEvent instance
        elif name in temp_films:
            ticketing_link = (f'http://www.cosfordcinema.com'
                              f'{film_tag.find_all("a", string=name)[0]["href"]}')
            start_time = film_tag.findNext('div').get_text().strip()
            showtime = FilmSchedule(dateutil.parser.parse(start_time),
                                    ticketing_link)
            # this conditional ensures that the link above is added to the
            # correct film
            for film in films:
                if name.title() == film.name:
                    film.showtimes.append(showtime)

    return films
