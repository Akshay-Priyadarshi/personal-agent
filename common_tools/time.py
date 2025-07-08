from datetime import datetime


def get_current_time() -> str:
    """Returns the current local time as an ISO string.

    Returns:
        str: The current local time in ISO format (HH:MM:SS).
    """
    return datetime.now().time().isoformat()
