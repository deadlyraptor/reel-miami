from datetime import datetime
from flask import Blueprint, render_template
from agile import AgileEvent
from rss import MBCEvent
from tower import fetch_tower_events
from reel_miami import Config

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    today = datetime.today().strftime('%Y-%m-%d')

    # Build the correct WebSales Feed URL.
    cgac_feed_url = AgileEvent.build_agile_payload(Config.CGAC_GUID, today)
    omb_feed_url = AgileEvent.build_agile_payload(Config.OMB_GUID, today)

    # Return the actual WebSales Feed (JSON).
    cgac_films = AgileEvent.fetch_agile_events(cgac_feed_url)
    omb_films = AgileEvent.fetch_agile_events(omb_feed_url)

    mbc_films = MBCEvent.fetch_mbc_events(today)

    tower_films = fetch_tower_events(today)

    return render_template('index.html', title='Home',
                           cgac_films=cgac_films,
                           omb_films=omb_films,
                           mbc_films=mbc_films,
                           tower_films=tower_films)
