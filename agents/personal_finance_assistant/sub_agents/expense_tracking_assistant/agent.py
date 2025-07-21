from typing import Any

from google.adk.agents import Agent, BaseAgent
from toolbox_core import ToolboxSyncClient

from agents.personal_finance_assistant.models import Expense, ExpenseCategory
from agents.personal_finance_assistant.tools.user import get_user_name
from common_models import BaseAdkAgent
from common_tools import get_current_date, get_current_time
from common_utils import FileUtils, StringUtils


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
        toolbox = ToolboxSyncClient(url='http://127.0.0.1:5000')
        pfa_tools = toolbox.load_toolset('pfa-toolset')
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
                get_user_name,
                get_current_date,
                get_current_time,
                *pfa_tools,
            ],
            before_agent_callback=self.before_agent_callback,
        )

    def test_prompts():
        prompts: list[str] = [
            'Please add an expense of 180 rs for a pack of cigarette today 10 am, category is Habits'  # noqa: E501
        ]
        return prompts


root_agent = ExpenseTrackingAssistant()
