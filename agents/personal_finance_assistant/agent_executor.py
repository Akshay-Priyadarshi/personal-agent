from a2a.server.agent_execution import RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState, TextPart, UnsupportedOperationError
from a2a.utils import new_agent_text_message, new_task
from a2a.utils.errors import ServerError
from google.adk.agents import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

from agents.personal_finance_assistant.tools import save_user_name
from common_models import BaseAdkAgentExecutor
from common_tools import get_current_date, get_current_time, google_search
from utils import FileUtils, LoggerUtils, StringUtils


logger = LoggerUtils.get_logger(__name__)


class PersonalFinancialAgentExecutor(BaseAdkAgentExecutor):
    """Agent executor for the Personal Financial Assistant agent.

    Inherits from ADKAgentExecutor to provide execution logic for handling
    personal finance-related tasks, such as expense tracking, budgeting,
    and financial analysis, within the A2A agent framework.
    """

    def __init__(self, initial_state: dict | None = None):
        super().__init__()
        self.initial_state = initial_state.copy() if initial_state else {}
        self.initial_state.setdefault('user:name', '')
        self.status_message = 'Processing your request...'
        self.artifact_name = 'response'

    def _build_instruction(self) -> str:
        return StringUtils.populate_variables(
            template_text=FileUtils.read_file_relative(
                __file__, 'instruction.md'
            ),
            variables={},
        )

    def _build_agent(self) -> LlmAgent:
        return LlmAgent(
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
        )

    def _build_runner(self) -> Runner:
        return Runner(
            app_name=self.agent.name,
            agent=self.agent,
            session_service=DatabaseSessionService(
                'sqlite:///./agents/personal_finance_assistant/adk.db'
            ),
            memory_service=InMemoryMemoryService(),
            artifact_service=InMemoryArtifactService(),
        )

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise ServerError(error=UnsupportedOperationError())

    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        user_id = 'awwwkshay'
        task = context.current_task
        if task is None:
            updater.submit()
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
