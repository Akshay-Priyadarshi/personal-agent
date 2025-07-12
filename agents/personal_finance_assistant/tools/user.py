from typing import Any

from google.adk.tools.tool_context import ToolContext

from common_models.tool_response import ToolResponse, ToolResponseStatus
from common_utils import LoggerUtils


logger = LoggerUtils.get_logger(__name__)


def save_user_name(
    new_user_name: str, tool_context: ToolContext
) -> dict[str, Any]:
    """Save the user name to the state.

    Args:
        new_user_name (str): The new user name to save.
        tool_context (ToolContext): The tool context containing the state.

    Returns:
        dict: A dictionary with keys like message, status and result.
        status: success, error, pending
        message: message from the tool
        result: dict of the outputs from tool
    """
    user_name_from_state = tool_context.state.get('user:name')
    tool_context.state['user:name'] = new_user_name
    response = ToolResponse(
        message='saved user name to state',
        status=ToolResponseStatus.success,
        result={
            'old_user_name': user_name_from_state,
            'new_user_name': new_user_name,
        },
    )
    logger.debug(
        'finalised tool response',
        extra={'tool_response': response.model_dump(mode='json')},
    )
    return response.model_dump(mode='json')


def get_user_name(tool_context: ToolContext) -> dict[str, Any]:
    """Retrieve the user name from the tool context state.

    Args:
        tool_context (ToolContext): The tool context containing the state.

    Returns:
        dict: A dictionary with keys like message, status, and result.
            - status: success, error, or pending
            - message: message from the tool
            - result: dict containing the user name
    """
    user_name_from_state = tool_context.state.get('user:name')
    response = ToolResponse(
        message='get user name from state',
        status=ToolResponseStatus.success,
        result={
            'user_name': user_name_from_state,
        },
    )
    logger.debug(
        'finalised tool response',
        extra={'tool_response': response.model_dump(mode='json')},
    )
    return response.model_dump(mode='json')
