from datetime import datetime
from flask import Blueprint, render_template
from ..feeds import agile, mbc, tower, cosford
from config import Config

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    today = datetime.today().strftime('%Y-%m-%d')

    cgac_films = agile.AgileEvent.fetch_agile_events(Config.CGAC_GUID, today)
    omb_films = agile.AgileEvent.fetch_agile_events(Config.OMB_GUID, today)

    mbc_films = mbc.MBCEvent.fetch_mbc_events(today)

    tower_films = tower.fetch_tower_events(today)

    cosford_films = cosford.fetch_cosford_events(today)

    return render_template('index.html', title='Home',
                           cgac_films=cgac_films,
                           omb_films=omb_films,
                           mbc_films=mbc_films,
                           tower_films=tower_films,
                           cosford_films=cosford_films)
