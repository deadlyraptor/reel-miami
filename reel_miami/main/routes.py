from datetime import datetime
from flask import Blueprint, render_template
from ..feeds import agile, mbc, tower, cosford
from config import Config

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    today = datetime.today().strftime('%Y-%m-%d')

    # Build the URLs needed to access the WebSales Feed.
    cgac_feed_url = agile.AgileEvent.build_agile_payload(Config.CGAC_GUID,
                                                         today)
    omb_feed_url = agile.AgileEvent.build_agile_payload(Config.OMB_GUID, today)

    # Return the actual WebSales Feed (JSON).
    cgac_films = agile.AgileEvent.fetch_agile_events(cgac_feed_url)
    omb_films = agile.AgileEvent.fetch_agile_events(omb_feed_url)

    mbc_films = mbc.MBCEvent.fetch_mbc_events(today)

    tower_films = tower.fetch_tower_events(today)

    cosford_films = cosford.fetch_cosford_events(today)

    return render_template('index.html', title='Home',
                           cgac_films=cgac_films,
                           omb_films=omb_films,
                           mbc_films=mbc_films,
                           tower_films=tower_films,
                           cosford_films=cosford_films)
