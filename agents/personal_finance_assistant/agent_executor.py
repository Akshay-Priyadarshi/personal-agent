import logging

from a2a.server.agent_execution import RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Role, TaskState, TextPart, UnsupportedOperationError
from a2a.utils import new_agent_text_message, new_task
from a2a.utils.errors import ServerError
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from agents.google_search_agent import google_search_assistant
from agents.personal_finance_assistant.tools import save_user_name
from common_models import BaseAdkAgentExecutor
from common_tools import get_current_date, get_current_time
from utils import FileUtils, StringUtils


logger = logging.getLogger(__file__)


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
                AgentTool(google_search_assistant),
            ],
            before_agent_callback=self.before_agent_callback,
        )

    def before_agent_callback(self, callback_context: CallbackContext):
        for key, value in self.initial_state.items():
            if callback_context.state.get(key, None) is None:
                callback_context.state[key] = value

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
        query = context.get_user_input()
        task = context.current_task or new_task(context.message)
        await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.contextId)
        user_id = 'awwwkshay'

        try:
            list_sessions_response = (
                await self.runner.session_service.list_sessions(
                    app_name=self.agent.name, user_id=user_id
                )
            )
            if len(list_sessions_response.sessions) > 0:
                session = list_sessions_response.sessions[0]
                logger.info(f'Using previous session with id {session.id}')
            else:
                session = await self.runner.session_service.create_session(
                    app_name=self.agent.name,
                    user_id=user_id,
                    state=self.initial_state,
                    session_id=task.contextId,
                )
                logger.info(f'New session created with id {session.id}')

            logger.info(f'context: {session.state}')

            message_content = types.Content(
                role=Role.user, parts=[types.Part.from_text(text=query)]
            )

            response_text = ''
            async for event in self.runner.run_async(
                user_id=user_id,
                session_id=session.id,
                new_message=message_content,
            ):
                if (
                    event.is_final_response()
                    and event.content
                    and event.content.parts
                ):
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text + '\n'
                        elif part.function_call:
                            # Log or handle function calls if needed
                            pass  # Function calls are handled internally by ADK

            # Send the final response as an artifact
            await updater.add_artifact(
                parts=[TextPart(text=response_text.strip())],
                name=self.artifact_name,
            )

            await updater.complete()

        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(
                    f'Error: {e!s}', task.contextId, task.id
                ),
                final=True,
            )
