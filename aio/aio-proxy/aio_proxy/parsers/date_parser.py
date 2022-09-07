from aio_proxy.decorators.value_exception import value_exception_handler
from datetime import date, datetime


@value_exception_handler(
    error="Veuillez indiquer une date sous le format : aaaa-mm-jj. Exemple : "
          "'1990-01-02'"
)
def parse_date(request, param: str, default_value=None):
    """Extract date param from request.

    Args:
        request: HTTP request
        param (str): parameter to extract from request
        default_value:

    Returns:
        None if None.
        param otherwise.
    """
    date_string = request.rel_url.query.get(param, default_value)
    if date_string is None:
        return None
    return date.fromisoformat(date_string)


@value_exception_handler(
    error="Veuillez indiquer une date minimale inférieure à la date maximale."
)
def validate_dates(min_date=None, max_date=None):
    if min_date and max_date:
        min_date = datetime.strptime(min_date, '%Y-%m-%d')
        max_date = datetime.strptime(max_date, '%Y-%m-%d')
        if max_date < min_date:
            raise ValueError
