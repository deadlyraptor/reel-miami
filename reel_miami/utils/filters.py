from flask import Blueprint

filters = Blueprint('filter', __name__)


@filters.app_template_filter()
def format_showtime(value):
    """Convert datetime object to string containing only the showtime.

    Example:
    YYYY-MM-DD H:M:S --> I:M:p
    1900-01-01 23:59:59 --> 11:59pm

    Parameters
    ----------
    value: datetime
        The date and time for the given screening.

    Returns
    -------
    showtime
        The showtime for the film, with am/pm in lowercase and stripped of
        leading 0.

    """
    showtime = value.strftime('%I:%M%p').lower().lstrip('0')
    return showtime


@filters.app_template_filter()
def format_date(value):
    """Format date object to a string.

    Parameters
    ----------
    value : date object
        The date to format.

    Returns
    -------
    date
        The date as month (abbreviated) and day of month as a number (stripped
        of leading zero).

    """
    date = value.strftime('%b %-d')
    return date


@filters.app_template_filter()
def format_day(value):
    """Format date object to a day string.

    Parameters
    ----------
    value : date object
        The date to format.

    Returns
    -------
    date
        The weekday as full name, e.g. Sunday.

    """
    date = value.strftime('%A')
    return date


@filters.app_template_filter()
def format_runtime(value):
    """Reformat the runtime of a film from minutes to hour & minutes.

    Parameters
    ---------
    value: str
        The runtime of the film in minutes.

    Returns
    -------
    runtime
        The runtime for the film formatted as X hr Y min.

    """
    runtime = f'{int(value) // 60} hr {int(value) % 60} min'
    return runtime
