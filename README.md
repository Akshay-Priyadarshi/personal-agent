# Personal Finance AI Agent

A modular, extensible AI agent system for personal finance management, built with Google ADK, Anthropic MCP, and Google A2A protocols. This project provides a personal finance assistant agent, a Google search agent, a personal assistant, and a framework for building and integrating additional agents and tools.

---

## Project Structure

```
personal-agent/
├── agents/                # Agent logic, including personal finance, search, and personal assistant agents
│   ├── __init__.py
│   ├── google_search_agent/
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── personal_assistant/     # General personal assistant agent
│   └── personal_finance_assistant/
│       ├── __init__.py
│       ├── a2a_app.py
│       ├── agent_executor.py
│       ├── agent.py
│       ├── instruction.md
│       ├── __main__.py         # Entry point for this specific agent
│       ├── adk.db              # Database file
│       └── tools/
│           └── __init__.py
├── clients/               # Client applications
│   └── cli/               # Command-line interface client
├── common_models/         # Shared models and base classes for agents and tools
│   ├── __init__.py
│   ├── base_adk_a2a_app.py
│   ├── base_adk_agent_executor.py
│   └── tool_response.py
├── common_tools/          # Shared utility tools (date, time, etc.)
│   ├── __init__.py
│   ├── date.py
│   └── time.py
├── utils/                 # Utility functions (environment, file, string helpers)
│   ├── __init__.py
│   ├── environment.py
│   ├── file.py
│   └── string.py
├── Makefile               # Build and workflow automation
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Lockfile for uv dependency manager
├── setup.bash             # Setup script
├── .python-version        # Python version specification
├── .ruff.toml            # Ruff linter configuration
├── .gitignore            # Git ignore rules
└── README.md              # Project overview and setup
```

### Directory Descriptions

- **agents/**: Agent logic, including the personal finance assistant, search agents, and personal assistant. Subfolders organize different agent types and their tools.
- **clients/**: Client applications, including the command-line interface.
- **common_models/**: Shared base classes and models for agents and tools.
- **common_tools/**: Utility tools (date, time, etc.) available to all agents.
- **utils/**: General-purpose utility functions (environment, file, string helpers).
- **Makefile**: Automation for common development tasks.
- **pyproject.toml**: Project configuration and dependencies.
- **uv.lock**: Lockfile for reproducible dependency installs with uv.
- **setup.bash**: Bash script for environment setup.
- **.python-version**: Python version specification for the project.
- **.ruff.toml**: Configuration for the Ruff linter.
- **.gitignore**: Git ignore rules for the project.
- **README.md**: Project overview, setup instructions, and documentation.

---

## Getting Started

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd personal-agent
   ```
2. **Install dependencies**
   ```sh
   uv sync
   ```
   If you don't have [uv](https://github.com/astral-sh/uv) installed:
   ```sh
   pip install uv
   # or see: https://github.com/astral-sh/uv#installation
   ```
3. **Set up environment variables**

   - Copy `.example.env` to `.env` in `agents/personal_finance_assistant/` and fill in any required values.

4. **Run the personal finance assistant agent**

   ```sh
   python -m agents.personal_finance_assistant
   # or
   cd agents/personal_finance_assistant && python __main__.py
   ```

   The server will start on `127.0.0.1:8080` by default.

5. **(Optional) Use the CLI client**
   ```sh
   python -m clients.cli
   ```
   This provides a command-line interface for interacting with the agents.

---

## Usage

- The personal finance assistant agent runs as a standalone service via the A2A protocol.
- Use the CLI client to interact with the agent, or integrate with other A2A-compatible tools.
- The agent can:
  - View account balances and recent transactions
  - Summarize spending by category and over time
  - Set and track budgets
  - Import transactions from files or integrations
  - Answer questions about your finances

---

## Agents Overview

### Personal Assistant

- **Location:** `agents/personal_assistant/`
- **Purpose:** General personal assistant capabilities for various tasks and queries.

### Personal Finance Assistant

- **Location:** `agents/personal_finance_assistant/`
- **Purpose:** Help users manage, understand, and improve their financial well-being.
- **Capabilities:**
  - Warmly greet and onboard users
  - Clarify user needs and financial goals
  - Categorize transactions and identify spending patterns
  - Summarize spending habits
  - Suggest personalized budgets and actionable advice
  - Provide visualizations and reports on request
  - Maintain a supportive, privacy-respecting, and transparent approach
- **See:** [`instruction.md`](agents/personal_finance_assistant/instruction.md) for full guidelines

### Google Search Agent

- **Location:** `agents/google_search_agent/`
- **Purpose:** Provide search capabilities to support the main agent or other use cases.

---

## Development & Contribution

- Code is organized for modularity and extensibility.
- Add new agents or tools by following the structure in `agents/` and `common_tools/`.
- Use the Makefile for common tasks (linting, formatting, etc.).
- Contributions are welcome! Please open issues or pull requests for improvements.

---

## License & Credits

Made with ❤️ in India

---

_This project is for educational and prototyping purposes. Not for production use or financial advice._
