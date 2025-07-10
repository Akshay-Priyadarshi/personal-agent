from typing import Any

from google.adk.tools.tool_context import ToolContext

from agents.personal_finance_assistant.models import ExpenseCategory
from common_models.tool_response import ToolResponse, ToolResponseStatus
from common_utils import LoggerUtils


logger = LoggerUtils.get_logger(__name__)


def add_expense_category(
    name: str,
    tool_context: ToolContext,
) -> dict[str, Any]:
    """Adds a new expense category to the user's list of expense categories in
    the tool context state.

    Args:
        name (str): The name of the expense category to add.
        tool_context (ToolContext): The tool context containing the current
        state.

    Returns:
        dict: A dictionary containing:
            - status (str): The status of the operation ('success', 'error',
            or 'pending').
            - message (str): A message describing the result of the operation.
            - result (dict): A dictionary with keys:
                - 'expenses_categories_before': The list of expense categories
                  before adding the new category.
                - 'expenses_categories_after': The list of expense categories
                after adding the new category.
    """
    new_expense_category = ExpenseCategory(name=name)

    raw_expense_categories: list[ExpenseCategory] = tool_context.state.get(
        'user:expense_categories'
    )
    expense_categories = [
        ExpenseCategory(**raw_expense_category)
        for raw_expense_category in raw_expense_categories
    ]
    updated_expense_categories = (
        [] if expense_categories is None else expense_categories.copy()
    )
    updated_expense_categories.append(new_expense_category)
    raw_updated_expense_categories = [
        expense_category.model_dump(mode='json')
        for expense_category in updated_expense_categories
    ]
    print(
        'state being updated with updated expense categories',
        raw_updated_expense_categories,
    )
    tool_context.state['user:expense_categories'] = (
        raw_updated_expense_categories
    )
    response = ToolResponse(
        message='added expense category to the list of expense categories',
        status=ToolResponseStatus.success,
        result={
            'expenses_categories_before': raw_expense_categories,
            'expenses_categories_after': raw_updated_expense_categories,
        },
    )
    logger.debug(
        'finalised tool response',
        extra={'tool_response': response.model_dump()},
    )
    return response.model_dump()
