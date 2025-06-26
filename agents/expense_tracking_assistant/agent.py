from google.adk.agents import LlmAgent

from common_tools import get_current_date, get_current_time
from expense_tracking_assistant.models import Expense
from utils import FileUtils, StringUtils


def _instruction_test() -> str:
    return StringUtils.populate_variables(
        template_text=FileUtils.read_file_relative(__file__, 'instruction.md'),
        variables={'expense_json_schema': Expense.model_json_schema()},
    )


root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='expense_tracking_assistant',
    description="""
    An agent designed to help users track and categorize expenses,
    identify trends, and provide actionable insights for better
    expense management.
    """,
    instruction=_instruction_test(),
    tools=[get_current_date, get_current_time],
)
