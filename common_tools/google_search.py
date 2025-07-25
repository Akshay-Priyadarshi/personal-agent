from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool


root_agent = Agent(
    model='gemini-2.0-flash',
    name='google_search_assistant',
    description="""
        An AI-powered assistant that leverages Google Search to,
        retrieve up-to-date information and answer user queries,
        by searching the web in real time.,
    """,
    instruction="""
    You are a google search assistant
    """,
    tools=[google_search],
)

google_search = AgentTool(root_agent)
