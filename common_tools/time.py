from datetime import datetime

from common_models import ToolResponse, ToolResponseStatus


def get_current_time() -> str:
    """Returns the current local time as an ISO string.

    Returns:
        str: The current local time in ISO format (HH:MM:SS).
    """
    current_time = datetime.now().time().isoformat()
    response = ToolResponse(
        message='retrieved current time',
        result={
            'current_time': current_time,
        },
        status=ToolResponseStatus.success,
    )
    return response.model_dump(mode='json')
