from datetime import date

from common_models import ToolResponse, ToolResponseStatus


def get_current_date() -> str:
    """Returns the current date as an ISO string.

    Returns:
        str: The current local date in ISO format (YYYY-MM-DD).
    """
    current_date = date.today().isoformat()
    response = ToolResponse(
        message='retrieved current date',
        result={
            'current_date': current_date,
        },
        status=ToolResponseStatus.success,
    )
    return response.model_dump(mode='json')
