import dateutil.parser
import requests
from bs4 import BeautifulSoup
from .film import FilmEvent, FilmSchedule
from config import Config


def fetch_cosford_events(date):
    """Fetch the HTML document for the Cosford Cinema website.

    Parameters
    ----------
    date : str
        The date to search for.

    Returns
    -------
    films
        A collection of instances of FilmEvent
    """
    r = requests.get(f'{Config.COSFORD_TIX}{date}')
    soup = BeautifulSoup(r.text, 'html.parser')

    films = []

    film_soup = soup.find_all('div', class_='views-field-title')
    for film_tag in film_soup:
        name = film_tag.get_text().title().strip()
        ticketing_link = f'http://www.cosfordcinema.com{film_tag.select("div a")[0]["href"]}'

        start_time = dateutil.parser.parse(film_tag.findNext('div').get_text().strip())
        showtimes = []
        showtimes.append(FilmSchedule(start_time, ticketing_link))

        film = FilmEvent(name, showtimes, ticketing_link)
        films.append(film)

    return films
