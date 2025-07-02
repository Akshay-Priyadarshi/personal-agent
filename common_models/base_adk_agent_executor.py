from abc import abstractmethod

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from google.adk.agents import LlmAgent
from google.adk.runners import Runner


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
    ):
        """Initialize a generic ADK agent executor.

        Args:
            agent: The ADK agent instance
            status_message: Message to display while processing
            artifact_name: Name for the response artifact
        """
        self.agent = self._build_agent()
        self.runner = self._build_runner()

    @abstractmethod
    def _build_instruction(self) -> str:
        raise NotImplementedError(
            'Subclasses must implement the _build_instruction method'
        )

    @abstractmethod
    def _build_agent(self) -> LlmAgent:
        raise NotImplementedError(
            'Subclasses must implement the _build_agent method'
        )

    @abstractmethod
    def _build_runner(self) -> Runner:
        raise NotImplementedError(
            'Subclasses must implement the _build_runner method'
        )

    @abstractmethod
    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancel the execution of a specific task."""
        raise NotImplementedError('Subclasses must implement the cancel method')

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
