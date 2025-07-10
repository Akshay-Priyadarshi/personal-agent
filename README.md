# Personal Assistant AI Agent

Personal Agent is a flexible, modular AI platform designed to help users manage their personal finances and daily tasks. Leveraging advanced protocols like Google ADK, Anthropic MCP, and Google A2A, the app features a suite of intelligent agents—including a personal finance assistant, and a general personal assistant. The system is built for extensibility, allowing developers to easily add new agents and tools to address a wide range of personal productivity and information needs. With a focus on user privacy, actionable insights, and seamless integration, Personal Agent empowers users to take control of their financial well-being and everyday life through conversational AI.

---

## Project Structure

```
personal-agent/
├── agents/                # Agent logic, including personal finance, search, and personal assistant agents
│   ├── __init__.py
│   ├── personal_finance_assistant/
│   │   ├── __init__.py
│   │   ├── a2a_app.py
│   │   ├── agent_executor.py
│   │   ├── agent.py
│   │   ├── instruction.md
│   │   ├── __main__.py
│   │   ├── Dockerfile
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── expense.py
│   │   ├── sub_agents/
│   │   │   ├── __init__.py
│   │   │   └── expense_tracking_assistant/
│   │   │       ├── __init__.py
│   │   │       ├── agent.py
│   │   │       ├── instruction.md
│   │   │       └── tools/
│   │   │           ├── __init__.py
│   │   │           ├── expense.py
│   │   │           └── expense_category.py
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── user.py
├── clients/               # Client applications
│   └── cli/
│       └── __main__.py
├── common_models/         # Shared models and base classes for agents and tools
│   ├── __init__.py
│   ├── base_adk_a2a_app.py
│   ├── base_adk_agent_executor.py
│   ├── base_adk_agent.py
│   └── tool_response.py
├── common_tools/          # Shared utility tools (date, time, google search, etc.)
│   ├── __init__.py
│   ├── date.py
│   ├── google_search.py
│   └── time.py
├── common_utils/          # Utility functions (environment, file, string helpers)
│   ├── __init__.py
│   ├── environment.py
│   ├── file.py
│   ├── logger.py
│   └── string.py
├── Makefile               # Build and workflow automation
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Lockfile for uv dependency manager
├── setup.bash             # Setup script
├── .python-version        # Python version specification
├── .ruff.toml             # Ruff linter configuration
├── .gitignore             # Git ignore rules
└── README.md              # Project overview and setup
```

### Directory Descriptions

- **agents/**: Agent logic, including the personal finance assistant, search agents, and personal assistant. Subfolders organize different agent types and their tools.
- **clients/**: Client applications, including the command-line interface.
- **common_models/**: Shared base classes and models for agents and tools.
- **common_tools/**: Utility tools (date, time, google search, etc.) available to all agents.
- **common_utils/**: General-purpose utility functions (environment, file, logger, string helpers).
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
2. **Setup Project**
   ```sh
   make setup
   ```
3. **Set up environment variables**

   - Copy `.example.env` to `.env` in `agents/personal_finance_assistant/` and fill in any required values.

4. **Run the Personal Finance Assistant agent**

   ```sh
   make run_local_personal_finance_assistant
   ```

   The server will start on `127.0.0.1:8080` by default.

5. **(Optional) Use the CLI client**
   ```sh
   make run_local_cli_client
   ```
   This provides a command-line interface for interacting with the agent.

---

## Makefile Commands for Local Development

You can use the following `make` commands to simplify local development and running the project:

- `make setup`  
  Run the setup script to prepare your environment.

- `make run_adk_web`  
  Start the ADK web interface for agents (for development/debugging).

- `make run_local_personal_finance_assistant`  
  Run the Personal Finance Assistant agent locally in development mode.

- `make build_personal_finance_assistant`  
  Build a Docker image for the Personal Finance Assistant agent.

- `make run_local_cli_client`  
  Run the CLI client locally to interact with the agent.

---

## Agents Overview

### Personal Finance Assistant

- **Location:** `agents/personal_finance_assistant/`
- **Description:**  
  A highly capable, friendly, and trustworthy personal finance assistant. Helps users manage, understand, and improve their financial well-being.
- **Capabilities:**
  - Warmly greet and onboard users, ask for and save their name.
  - Clarify user needs and financial goals.
  - Categorize transactions, identify spending patterns, and summarize spending habits.
  - Suggest personalized budgets and actionable advice.
  - Provide visualizations and reports on request.
  - Maintain a supportive, privacy-respecting, and transparent approach.
  - **Sub-agents:**
    - **Expense Tracking Assistant** (see below)
  - **Tools:**
    - `get_current_date`: Returns the current date.
    - `get_current_time`: Returns the current time.
    - `save_user_name`: Saves the user's name to state.

#### Sub-Agent: Expense Tracking Assistant

- **Location:** `agents/personal_finance_assistant/sub_agents/expense_tracking_assistant/`
- **Description:**  
  Specialized in tracking and analyzing user expenses.
- **Capabilities:**
  - Log new expenses and categorize transactions.
  - View summaries and generate reports to gain insights into spending habits.
  - Infer categories and dates from user input when possible.
  - Confirm and validate all expense data before saving.
  - Provide clear, actionable spending reports.
  - **Tools:**
    - `get_current_date`: Returns the current date.
    - `get_current_time`: Returns the current time.
    - `add_expense`: Adds a new expense to the user's list.
    - `add_expense_category`: Adds a new expense category to the user's list.

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
