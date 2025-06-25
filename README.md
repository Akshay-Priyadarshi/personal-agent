# Personal Finance AI Agent

A sample project structure for a Personal Finance AI Agent using Google ADK, Anthropic MCP, and Google A2A protocols.

## Project Structure

```
personal-finance-agent/
├── agent/                # ADK agent code (main agent logic, intents, state)
│   ├── __init__.py
│   ├── main_agent.py
│   └── ...
├── tools/                # MCP tools (categorizer, summarizer, etc.)
│   ├── __init__.py
│   ├── transaction_categorizer.py
│   └── ...
├── integrations/         # A2A connectors (mock bank agent, tax agent, etc.)
│   ├── __init__.py
│   ├── bank_agent.py
│   └── ...
├── ui/                   # Simple web or CLI UI (optional)
│   ├── __init__.py
│   ├── app.py
│   └── ...
├── data/                 # Sample/mock data for development
│   ├── transactions_sample.json
│   └── ...
├── requirements.txt      # Python dependencies
└── README.md             # Project overview and setup
```

## Directory Descriptions

- **agent/**: Main ADK agent code, including intent handling and state management.
- **tools/**: MCP tools for modular capabilities (e.g., transaction categorization, budgeting).
- **integrations/**: A2A protocol connectors for external agents (e.g., bank, tax, investment agents).
- **ui/**: Optional user interface (web or CLI) for interacting with the agent.
- **data/**: Mock or sample data for development and testing.

## Getting Started

1. Clone the repository.
2. Install dependencies: `uv sync`
   - If you don't have [uv](https://github.com/astral-sh/uv) installed, you can install it with `pip install uv` or follow the instructions in the [uv documentation](https://github.com/astral-sh/uv#installation).
3. Run the main agent: `python agent/main_agent.py`

---

You can expand each directory as you add more features, tools, and integrations.
