from datetime import datetime
from typing import Any

from google.adk.tools.tool_context import ToolContext

from agents.personal_finance_assistant.models import Expense, ExpenseCategory
from common_models.tool_response import ToolResponse, ToolResponseStatus
from common_utils import LoggerUtils


logger = LoggerUtils.get_logger(__name__)


def add_expense(
    description: str,
    amount: float,
    date: str,
    time: str,
    category_name: str,
    tool_context: ToolContext,
) -> dict[str, Any]:
    """Adds a new expense to the user's list of expenses in the tool
    context state.

    Args:
        description (str): The description of the expense.
        amount (float): The amount of the expense.
        date (str): The date of the expense in ISO format (YYYY-MM-DD).
        time (str): The time of the expense in ISO format (HH:MM:SS).
        category_name (str): The name of the expense category.
        tool_context (ToolContext): The tool context containing the current state.

    Returns:
        dict: A dictionary containing:
            - status (str): The status of the operation ('success', 'error',
              or 'pending').
            - message (str): A message describing the result of the operation.
            - result (dict): A dictionary with keys:
                - 'expenses_before': The list of expenses before adding the
                new expense.
                - 'expenses_after': The list of expenses after adding the new
                expense.
    """
    logger.info(
        f'description: {description}, amount: {amount}, date: {date}, time: {time}, category_name: {category_name}'
    )
    new_expense = Expense(
        description=description,
        amount=amount,
        date=datetime.fromisoformat(date).date(),
        time=datetime.strptime(time, '%H:%M:%S').time(),
        category=ExpenseCategory(name=category_name),
    )
    raw_expenses: list[dict] = tool_context.state.get('user:expenses')
    expenses = [Expense(**raw_expense) for raw_expense in raw_expenses]
    updated_expenses: list[Expense] = (
        [] if expenses is None else expenses.copy()
    )
    updated_expenses.append(new_expense)
    raw_updated_expenses = [
        expense.model_dump(mode='json') for expense in updated_expenses
    ]
    print('state being updated with updated expenses', raw_updated_expenses)
    tool_context.state['user:expenses'] = raw_updated_expenses
    response = ToolResponse(
        message='added expense to the list of expenses',
        status=ToolResponseStatus.success,
        result={
            'expenses_before': raw_expenses,
            'expenses_after': raw_updated_expenses,
        },
    )
    logger.debug(
        'finalised tool response',
        extra={'tool_response': response.model_dump()},
    )
    return response.model_dump()
