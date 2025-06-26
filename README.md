<h1>Personal Finance AI Agent</h1>
<p>
A sample project structure for a Personal Finance AI Agent using Google ADK, Anthropic MCP, and Google A2A protocols.
</p>
<h2>Project Structure</h2>

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

<h2>Directory Descriptions</h2>

- <b>agent/</b>: Main ADK agent code, including intent handling and state management.
- <b>tools/</b>: MCP tools for modular capabilities (e.g., transaction categorization, budgeting).
- <b>integrations/</b>: A2A protocol connectors for external agents (e.g., bank, tax, investment agents).
- <b>ui/</b>: Optional user interface (web or CLI) for interacting with the agent.
- <b>data/</b>: Mock or sample data for development and testing.

<h2>Getting Started</h2>
<ol>
   <li>Clone the repository</li>
   <li>
      <p>Install dependencies: `uv sync`</p>
      <ul>
         <li>
            If you don't have [uv](https://github.com/astral-sh/uv) installed, you can install it with `pip install uv` or follow the instructions in the [uv documentation](https://github.com/astral-sh/uv#installation).
         </li>
      </ul>
   </li>
   <li>Run the main agent: `python agent/main_agent.py`</li>
</ol>

<h2>Agents</h2>
<ol>
   <div>
      <h3>
         <li>
            Personal Finance Assistant
         </li>
      </h3>
      <p>
         This is the main agent which will be used to interact with personal finance agent. 
      </p>
      <h4>Capabilities</h4>
      <ul>
         <li>View account balances and recent transactions</li>
         <li>Summarize spending by category and over time</li>
         <li>Set and track budgets</li>
         <li>Import transactions from files or integrations</li>
         <li>Answer questions about your finances</li>
      </ul>
   </div>
   <div>
      <h3>
         <li>
            Expense Tracking Assistant
         </li>
      </h3>
      <p>
         Helps track the expenses for the user.
      </p>
      <h4>Capabilities</h4>
      <ul>
         <li>Add and categorize new expenses</li>
         <li>View and search expense history</li>
         <li>Generate expense reports by category or date</li>
         <li>Detect duplicate or unusual expenses</li>
      </ul>
   </div>
</ol>

---

Made with ❤️ from India
