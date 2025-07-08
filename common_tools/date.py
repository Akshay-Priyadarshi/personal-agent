from datetime import date


def get_current_date() -> str:
    """Returns the current date as an ISO string.

    Returns:
        str: The current local date in ISO format (YYYY-MM-DD).
    """
    return date.today().isoformat()
