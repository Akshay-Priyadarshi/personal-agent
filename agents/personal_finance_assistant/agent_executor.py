from typing import override

from a2a.server.agent_execution import RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState, TextPart, UnsupportedOperationError
from a2a.utils import new_agent_text_message, new_task
from a2a.utils.errors import ServerError
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

from agents.personal_finance_assistant.agent import PersonalFinanceAssistant
from common_models import BaseAdkAgentExecutor
from common_models.base_adk_agent import BaseAdkAgent
from common_utils import LoggerUtils


logger = LoggerUtils.get_logger(__name__)


class PersonalFinancialAgentExecutor(BaseAdkAgentExecutor):
    """Agent executor for the Personal Financial Assistant agent.

    Inherits from ADKAgentExecutor to provide execution logic for handling
    personal finance-related tasks, such as expense tracking, budgeting,
    and financial analysis, within the A2A agent framework.
    """

    def __init__(self, initial_state: dict | None = None):
        self.initial_state = initial_state.copy() if initial_state else {}
        self.initial_state.setdefault('user:name', '')
        super().__init__()
        self.status_message = 'Processing your request...'
        self.artifact_name = 'response'

    @override
    def _build_agent(self) -> BaseAdkAgent:
        return PersonalFinanceAssistant(initial_state=self.initial_state)

    @override
    def _build_runner(self) -> Runner:
        return Runner(
            app_name=self.adk_agent.name,
            agent=self.adk_agent,
            session_service=DatabaseSessionService(
                'sqlite:///./agents/personal_finance_assistant/adk.db'
            ),
            memory_service=InMemoryMemoryService(),
            artifact_service=InMemoryArtifactService(),
        )

    @override
    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise ServerError(error=UnsupportedOperationError())

    @override
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        user_id = 'awwwkshay'
        task = context.current_task
        if task is None:
            await updater.submit()
            task = new_task(context.message)

        await updater.event_queue.enqueue_event(task)
        await updater.start_work()

        try:
            # get app session
            session = await self.get_app_session(
                context=context, user_id=user_id
            )

            # get user message content
            user_message_content = await self.get_user_message_content(
                context=context
            )

            # get agent response text with the user content
            agent_response_text = await self.get_agent_response_text(
                session_id=session.id,
                user_id=user_id,
                user_message_content=user_message_content,
            )

            # send the final response as an artifact
            await updater.add_artifact(
                parts=[TextPart(text=agent_response_text)],
                name=self.artifact_name,
            )

            # send task completed
            await updater.complete()
        except Exception as e:
            logger.exception(e)
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(
                    f'Error: {e!s}', task.contextId, task.id
                ),
                final=True,
            )
