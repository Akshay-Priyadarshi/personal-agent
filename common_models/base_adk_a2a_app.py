from abc import ABC, abstractmethod

import uvicorn

from a2a.server.apps import A2AFastAPIApplication, JSONRPCApplication
from a2a.server.request_handlers import DefaultRequestHandler, RequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from common_models.base_adk_agent_executor import BaseAdkAgentExecutor


class BaseAdkA2AApp(ABC):
    """Base class for ADK applications in the A2A framework.

    This class provides a foundation for creating ADK (Agent Development Kit)
    applications that can be integrated with the A2A (Agent-to-Agent) framework.
    It serves as a common interface and provides shared functionality for
    all ADK application implementations.

    The BaseAdkApp class is designed to be inherited by specific application
    implementations, providing them with the necessary structure and
    capabilities to work within the A2A ecosystem while leveraging the
    Google ADK for application development.

    The class manages the core components of an A2A application:
    - Agent card (metadata and capabilities)
    - Request handler (for processing incoming requests)
    - A2A application (the main application instance)

    Subclasses must implement the abstract methods to provide specific
    functionality for their application domain.
    """

    def __init__(self) -> None:
        self.agent_executor = self._build_agent_executor()
        self.agent_card = self._build_agent_card()
        self.a2a_app = self._build_a2a_app()

    @abstractmethod
    def _build_agent_executor(self) -> BaseAdkAgentExecutor:
        raise NotImplementedError(
            'Subclasses must implement the _build_agent_executor method'
        )

    @abstractmethod
    def _build_agent_skills(self) -> list[AgentSkill]:
        raise NotImplementedError(
            'Subclasses must implement the _build_agent_skills method'
        )

    @abstractmethod
    def _build_agent_capabilities(self) -> AgentCapabilities:
        raise NotImplementedError(
            'Subclasses must implement the _build_agent_capabilities method'
        )

    @abstractmethod
    def _build_agent_card(self) -> AgentCard:
        raise NotImplementedError(
            'Subclasses must implement the _build_agent_card method'
        )

    def _build_request_handler(self) -> RequestHandler:
        return DefaultRequestHandler(
            agent_executor=self.agent_executor,
            task_store=InMemoryTaskStore(),
        )

    def _build_a2a_app(self) -> JSONRPCApplication:
        return A2AFastAPIApplication(
            agent_card=self.agent_card,
            http_handler=self._build_request_handler(),
        )

    def start(self, host: str, port: int) -> None:
        uvicorn.run(self.a2a_app.build(), host=host, port=port)
