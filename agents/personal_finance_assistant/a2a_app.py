from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from agents.personal_finance_assistant.agent_executor import (
    PersonalFinancialAgentExecutor,
)
from common_models import BaseAdkA2AApp
from common_models.base_adk_agent_executor import BaseAdkAgentExecutor
from common_utils import EnvironmentUtils


class PersonalFinanceA2AApp(BaseAdkA2AApp):
    """A2A application for personal finance assistance.

    This application provides a conversational interface for personal
    finance advice, including budgeting, saving, investing, debt management,
    and financial planning. It leverages AI to offer personalized financial
    guidance and help users develop healthy money habits.
    """

    def __init__(self) -> None:
        super().__init__()

    def _build_agent_executor(self) -> BaseAdkAgentExecutor:
        return PersonalFinancialAgentExecutor(initial_state={'user:name': ''})

    def _build_agent_skills(self) -> list[AgentSkill]:
        return [
            AgentSkill(
                id='give_personal_finance_advice',
                name='Give Personal Finance Advice',
                description=(
                    'Provides personalized financial advice and guidance on '
                    'budgeting, saving, investing, debt management, and other '
                    'personal finance topics. Can help users make informed '
                    'financial decisions and develop healthy money habits.'
                ),
                tags=['finance', 'advice', 'budgeting', 'investing', 'debt'],
                examples=[''],
            )
        ]

    def _build_agent_capabilities(self) -> AgentCapabilities:
        return AgentCapabilities()

    def _build_agent_card(self) -> AgentCard:
        app_host = EnvironmentUtils.read_env_var('APP_HOST')
        app_port = EnvironmentUtils.read_env_var('APP_PORT')
        return AgentCard(
            name=self.agent_executor.adk_agent.name,
            description=self.agent_executor.adk_agent.description,
            skills=self._build_agent_skills(),
            url=f'{app_host}:{app_port}/',
            version='1.0.0',
            defaultInputModes=['text', 'text/plain'],
            defaultOutputModes=['text', 'text/plain'],
            capabilities=AgentCapabilities(streaming=True),
        )
