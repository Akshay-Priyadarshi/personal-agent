from typing import Any

from google.adk.agents import Agent, BaseAgent

from agents.personal_finance_assistant.sub_agents import (
    ExpenseTrackingAssistant,
)
from agents.personal_finance_assistant.tools import save_user_name
from common_models import BaseAdkAgent
from common_tools import get_current_date, get_current_time, google_search
from utils import FileUtils, StringUtils


class PersonalFinanceAssistant(BaseAdkAgent):
    """The PersonalFinanceAssistant is an ADK agent designed to help users
    manage their personal finances. It provides capabilities such as expense
    tracking, budgeting, financial analysis, and personalized advice. The
    agent leverages sub-agents and tools to assist users in understanding
    and improving their financial well-being.
    """

    def __init__(self, initial_state: dict[str, Any] = None):
        super().__init__(initial_state)

    def _build_agent(self) -> BaseAgent:
        return Agent(
            model='gemini-2.0-flash',
            name='personal_finance_assistant',
            description="""
You are a personal finance assistant that helps users manage
their money effectively. You can track expenses, create
budgets, provide financial analysis, and offer personalized
financial advice to improve their financial well-being.
            """,
            instruction=self._build_instruction(),
            tools=[
                get_current_date,
                get_current_time,
                save_user_name,
                google_search,
            ],
            before_agent_callback=self.before_agent_callback,
            sub_agents=[
                ExpenseTrackingAssistant(
                    initial_state={
                        'user:expenses': [],
                        'user:expense_categories': [],
                    }
                ).adk_agent
            ],
        )

    def _build_instruction(self) -> str:
        return StringUtils.populate_variables(
            template_text=FileUtils.read_file_relative(
                __file__, 'instruction.md'
            ),
            variables={},
        )


root_agent = PersonalFinanceAssistant(initial_state={'user:name': ''}).adk_agent
