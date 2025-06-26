from datetime import date


def get_current_date() -> date:
    """Returns the current date.

    Returns:
        date: The current local date.
    """
    return date.today()
