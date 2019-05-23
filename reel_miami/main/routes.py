from datetime import date, timedelta
import dateutil
from flask import Blueprint, render_template, request
from ..feeds import agile, mbc, tower, cosford
from config import Config

main = Blueprint('main', __name__)


@main.context_processor
def context_processor():
    """Add the current day to all templates.

    Used for the datepicker at the top of the index page. Python's timedelta
    is also passed to the processor so the subsequent dates can be added to the
    datepicker buttons.
    """
    today = date.today()

    return dict(today=today, timedelta=timedelta)


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def index():
    """Render the index/home page.

    All venue feeds are called in order to render the template with data.
    """
    if request.method == 'POST':
        date_to_seek = dateutil.parser.parse(request.form['date'])
    else:
        date_to_seek = date.today()

    cgac_films = agile.AgileEvent.fetch_agile_events(Config.CGAC_GUID,
                                                     date_to_seek)
    omb_films = agile.AgileEvent.fetch_agile_events(Config.OMB_GUID,
                                                    date_to_seek)

    mbc_films = mbc.MBCEvent.fetch_mbc_events(date_to_seek)

    tower_films = tower.fetch_tower_events(date_to_seek)

    cosford_films = cosford.fetch_cosford_events(date_to_seek)

    return render_template('index.html', title='Home',
                           cgac_films=cgac_films,
                           omb_films=omb_films,
                           mbc_films=mbc_films,
                           tower_films=tower_films,
                           cosford_films=cosford_films)
