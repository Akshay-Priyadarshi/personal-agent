from enum import Enum
from typing import Any

from pydantic import BaseModel


class ToolResponseStatus(str, Enum):
    """Enumeration of possible statuses for a tool response."""

    success = 'success'
    pending = 'pending'
    error = 'error'


class ToolResponse(BaseModel):
    """Represents the response from a tool execution.

    Attributes:
        status (ToolResponseStatus): The status of the tool response
        (success, pending, or error).
        data (DataType): The data returned by the tool, of a generic type.
        message (str): An optional message providing additional information
        about the response.
    """

    status: ToolResponseStatus
    result: dict[str, Any]
    message: str
