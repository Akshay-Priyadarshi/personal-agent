from abc import abstractmethod

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Role, Task, TaskState
from a2a.utils import new_agent_text_message
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import Runner
from google.adk.sessions import Session
from google.genai import types

from common_models.base_adk_agent import BaseAdkAgent
from common_utils import LoggerUtils


logger = LoggerUtils.get_logger(
    name=__name__,
)


class BaseAdkAgentExecutor(AgentExecutor):
    """An executor for running ADK agents within the A2A framework.

    This class integrates an ADK agent with the A2A agent execution
    infrastructure, handling task execution, event queuing, and status
    updates. It provides methods for executing and (optionally) canceling
    agent tasks, and manages in-memory services for artifacts, sessions,
    and memory.
    """

    def __init__(
        self,
        initial_state: dict | None = None,
    ):
        """Initialize a generic ADK agent executor.
            initial_state (dict | None): Optional initial state for the agent
            executor.

        Attributes:
            initial_state (dict | None): Stores the initial state.
            agent: The built agent instance.
            adk_agent: The ADK agent extracted from the built agent.
            runner: The runner instance built for executing the agent.
        """
        self.initial_state = initial_state
        self.agent = self._build_agent()
        self.adk_agent = self.agent.adk_agent
        self.runner = self._build_runner()

    @abstractmethod
    def _build_agent(self) -> BaseAdkAgent:
        raise NotImplementedError(
            'Subclasses must implement the _build_agent method'
        )

    @abstractmethod
    def _build_runner(self) -> Runner:
        raise NotImplementedError(
            'Subclasses must implement the _build_runner method'
        )

    def before_agent_callback(self, callback_context: CallbackContext):
        for key, value in self.initial_state.items():
            if callback_context.state.get(key, None) is None:
                callback_context.state[key] = value

    @abstractmethod
    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancel the execution of a specific task."""
        raise NotImplementedError('Subclasses must implement the cancel method')

    async def get_app_session(
        self, context: RequestContext, user_id: str
    ) -> Session:
        try:
            old_session = await self.runner.session_service.get_session(
                app_name=self.adk_agent.name,
                user_id=user_id,
                session_id=context.context_id,
            )
            if old_session:
                session = old_session
                logger.debug(
                    f'Using old session with id {session.id}',
                    extra={'old_session': session.model_dump()},
                )
            else:
                session = await self.runner.session_service.create_session(
                    app_name=self.adk_agent.name,
                    user_id=user_id,
                    state=self.initial_state,
                    session_id=context.context_id,
                )
                logger.debug(
                    f'New session created with id {session.id}',
                    extra={'new_session': session.model_dump()},
                )
            return session
        except Exception as e:
            logger.exception(e)
            raise e

    async def get_user_message_content(
        self, context: RequestContext
    ) -> types.Content:
        user_query = context.get_user_input().strip()
        if not user_query or (user_query and user_query == ''):
            logger.warning('user query appears to be none or empty')
            raise Exception('user query appears to be none or empty')
        return types.Content(
            role=Role.user, parts=[types.Part.from_text(text=user_query)]
        )

    async def get_agent_response_text(
        self,
        session_id: str,
        user_id: str,
        user_message_content: types.Content,
        updater: TaskUpdater,
        task: Task
    ) -> str:
        response_text = ''
        async for event in self.runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message_content,
        ):
            logger.info("event recieved from agent", extra={"event":event})
            if (
                event.is_final_response()
                and event.content
                and event.content.parts
            ):
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text + '\n'
                    elif part.function_call:
                        await updater.update_status(
                            TaskState.working,
                            new_agent_text_message(
                                f"Calling function `{part.function_call.name}`",
                                session_id,
                                task.id
                            )
                        )
                    elif part.file_data:
                        file_mime_type = part.file_data.mime_type
                        logger.info(
                            f"file type part with mime type '{file_mime_type}'received"
                        )
        return response_text.strip()

    @abstractmethod
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute a specific task."""
        raise NotImplementedError(
            'Subclasses must implement the execute method'
        )
