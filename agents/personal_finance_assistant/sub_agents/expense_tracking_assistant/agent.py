from typing import Any

from google.adk.agents import Agent, BaseAgent

from agents.personal_finance_assistant.models import Expense, ExpenseCategory
from agents.personal_finance_assistant.sub_agents.expense_tracking_assistant.tools import (  # noqa: E501
    add_expense,
    add_expense_category,
)
from common_models import BaseAdkAgent
from common_tools import get_current_date, get_current_time
from utils import FileUtils, StringUtils


class ExpenseTrackingAssistant(BaseAdkAgent):
    """The ExpenseTrackingAssistant is a specialized ADK agent for
    tracking and analyzing user expenses.

    This assistant enables users to log new expenses, categorize
    transactions, view summaries, and generate reports to gain
    insights into their spending habits. It leverages the Expense
    and ExpenseCategory schemas to structure financial data and
    provides a conversational interface for personal finance management.
    """

    def __init__(self, initial_state: dict[str, Any] = None):
        super().__init__(initial_state)

    def _build_instruction(self) -> str:
        return StringUtils.populate_variables(
            template_text=FileUtils.read_file_relative(
                __file__, 'instruction.md'
            ),
            variables={
                'expense_schema': Expense.model_json_schema(),
                'expense_category_schema': ExpenseCategory.model_json_schema(),
            },
        )

    def _build_agent(self) -> BaseAgent:
        return Agent(
            model='gemini-2.0-flash',
            name='expense_tracking_assistant',
            description="""
            The Expense Tracking Assistant helps users monitor, categorize,
            and analyze their spending. It allows users to log expenses,
            view summaries by category or time period, and receive insights
            to improve their financial habits. The assistant supports adding
            new expenses, querying past transactions, and generating reports
            to help users stay on top of their personal finances.
            """,
            instruction=self._build_instruction(),
            tools=[
                get_current_date,
                get_current_time,
                add_expense,
                add_expense_category,
            ],
            before_agent_callback=self.before_agent_callback,
        )

    def test_prompts():
        prompts: list[str] = [
            'Please add an expense of 180 rs for a pack of cigarette today 10 am, category is Habits'
        ]
        return prompts


root_agent = ExpenseTrackingAssistant(
    initial_state={'user:expenses': [], 'user:expense_categories': []}
)
