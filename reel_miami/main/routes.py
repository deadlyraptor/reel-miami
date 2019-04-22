from datetime import datetime
from flask import Blueprint, render_template
from agile import build_agile_venue_url, fetch_events
from reel_miami import Config

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    today = (
             f'{datetime.today().year}-'
             f'{datetime.today().month}-'
             f'{datetime.today().day}'
             )
    # Build the correct WebSales Feed URL.
    cgac_feed_url = build_agile_venue_url(Config.CGAC_GUID, today)
    omb_feed_url = build_agile_venue_url(Config.OMB_GUID, today)

    # Return the actual WebSales Feed (JSON).
    cgac_films = fetch_events(cgac_feed_url)
    omb_films = fetch_events(omb_feed_url)
    return render_template('index.html', title='Home', cgac_films=cgac_films,
                           omb_films=omb_films)
