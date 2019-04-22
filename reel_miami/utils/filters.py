from flask import Blueprint

filters = Blueprint('filter', __name__)


@filters.app_template_filter()
def format_showtime(value, format=('%I:%M%p')):
    """Converts datetime object to string containing only the showtime.

    Example:
    YYYY-MM-DD H:M:S --> I:M:p
    1900-01-01 23:59:59 --> 11:59pm

    Parameters
    ----------
    value: datetime
        The date and time for the given showtime.
    format: str
        The format string.

    Returns
    -------
    str
        The showtime for the film.
    """

    return value.strftime(format).lower().lstrip('0')
