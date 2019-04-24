from flask import Blueprint

filters = Blueprint('filter', __name__)


@filters.app_template_filter()
def format_showtime(value):
    """Converts datetime object to string containing only the showtime.

    Example:
    YYYY-MM-DD H:M:S --> I:M:p
    1900-01-01 23:59:59 --> 11:59pm

    Parameters
    ----------
    value: datetime
        The date and time for the given showtime.

    Returns
    -------
    str
        The showtime for the film, with am/pm in lowercase and stripped of
        leading 0.
    """

    showtime = value.strftime('%I:%M%p').lower().lstrip('0')
    return showtime


@filters.app_template_filter()
def format_runtime(value):
    """

    Parameters
    ---------
    value: str
        The runtime of the film in minutes.

    Returns
    -------
    str
        The runtime for the film formatted as X hr Y min.
    """

    runtime = f'{int(value) // 60} hr {int(value) % 60} min'
    return runtime
