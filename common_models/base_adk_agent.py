from abc import ABC, abstractmethod
from typing import Any

from google.adk.agents import BaseAgent
from google.adk.agents.callback_context import CallbackContext

from common_utils import LoggerUtils


logger = LoggerUtils.get_logger(
    name=__name__,
)


class BaseAdkAgent(ABC):
    """Base class for ADK agents using Pydantic models.

    This class provides a structure for defining agents with an
    instruction and an ADK agent instance.
    Subclasses must implement methods to build the agent's instruction
    and the ADK agent itself.

    Attributes:
        instruction (str): The instruction or prompt for the agent.
        adk_agent (BaseAgent): The underlying ADK agent instance.
    """

    def __init__(self, initial_state: dict[str, Any] = None):
        super().__init__()
        self.initial_state = {} if initial_state is None else initial_state
        self.instruction = self._build_instruction()
        self.adk_agent = self._build_agent()

    @abstractmethod
    def _build_instruction(self) -> str:
        raise NotImplementedError(
            'Subclasses must implement the _build_instruction method'
        )

    def before_agent_callback(self, callback_context: CallbackContext):
        for key, value in self.initial_state.items():
            if callback_context.state.get(key, None) is None:
                callback_context.state[key] = value

    @abstractmethod
    def _build_agent(self) -> BaseAgent:
        raise NotImplementedError(
            'Subclasses must implement the _build_agent method'
        )
