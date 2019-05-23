import dateutil.parser
import requests
from bs4 import BeautifulSoup
from .film import FilmEvent, FilmSchedule
from config import Config


def fetch_tower_events(today):
    """Fetch the HTML document from Tower Theater's Veezi ticketing page.

    The parameter is used to focus on a specific date as the HTML document
    contains the full schedule for the venue, including multiple dates of
    screenings.

    Parameters
    ----------
    today : str
        A date in the format YYYY-M-D.

    Returns
    -------
    list
        A collection of instances of FilmEvent.

    """
    r = requests.get(Config.TOWER_TIX)
    soup = BeautifulSoup(r.text, 'html.parser')

    # The date passed in by the route is in a format different from the date
    # string in the HTML document so the passed in date has to be reformatted
    # to match the HTML document's version.
    new_today = today.strftime('%A %-d, %B')

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

                # this gets the showtimes and corresponding ticketing links
                sessions = film_tag.find('ul', class_='session-times')
                li_tags = sessions.find_all('li')
                showtimes = []
                for li_tag in li_tags:
                    # the li tag only has the start time so we build a
                    # 'datetime' string and pass it into the dateutil parser in
                    # order to create a datetime object with a date
                    start_time = dateutil.parser.parse(f'{date.get_text()} {li_tag.a.time.get_text()}')
                    buy_link = li_tag.a['href']
                    # for every showtime, create an instance of FilmSchedule
                    showtime = FilmSchedule(start_time, buy_link)
                    showtimes.append(showtime)
                # create a new instance of FilmEvent during every loop of the
                # film divs
                film = FilmEvent(name, showtimes)
                films.append(film)

    return films
