from datetime import date, timedelta

import dateutil
from flask import Blueprint, current_app, flash, redirect, render_template, \
    request, url_for

from ..feeds import agile, cosford, mbc, tower
from reel_miami.models import Venue

main = Blueprint('main', __name__)


@main.context_processor
def context_processor():
    """Add the current day to all templates.

    Used for the datepicker at the top of the index page. Python's timedelta
    is also passed to the processor so the subsequent dates can be added to the
    datepicker buttons.
    """
    today = date.today()

    return {'today': today, 'timedelta': timedelta}


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

    cgac_films = agile.AgileEvent.fetch_agile_events(current_app.config['CGAC_GUID'],
                                                     date_to_seek)
    omb_films = agile.AgileEvent.fetch_agile_events(current_app.config['OMB_GUID'],
                                                    date_to_seek)

    cosford_films = cosford.fetch_cosford_events(date_to_seek)
    mbc_films = mbc.MBCEvent.fetch_mbc_events(date_to_seek)
    tower_films = tower.fetch_tower_events(date_to_seek)

    return render_template('index.html', title='Home',
                           cgac_films=cgac_films,
                           omb_films=omb_films,
                           mbc_films=mbc_films,
                           tower_films=tower_films,
                           cosford_films=cosford_films)


@main.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', title='About')


@main.route('/venues')
def venues():
    """Render the venue directory page."""
    venues = Venue.query.order_by(Venue.name).all()

    if not venues:
        flash('No venues found.', 'warning')
        return redirect(url_for('main.index'))

    return render_template('venue-directory.html', title='Venues',
                           venues=venues)


@main.route('/venue/<int:id>')
def venue(id):
    """Render the page for a venue."""
    venue = Venue.query.filter_by(id=id).first_or_404()

    if not venue:
        flash('No venue found.', 'warning')
        return redirect(url_for('main.venues'))

    venue_photo = url_for('static',
                          filename=f'img/venues/{venue.venue_photo}')

    return render_template('venue-listing.html', venue=venue,
                           venue_photo=venue_photo, title=venue.name)


@main.route('/admin')
def admin():
    """Redirect to the Flask-Admin index page."""
    return redirect(url_for('main.admin'))
