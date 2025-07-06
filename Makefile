setup:
	bash setup.bash

run_adk_web:
	PYTHONPATH=. adk web ./agents

run_local_personal_finance_assistant:
	APP_ENV=development PYTHONPATH=. uv run agents/personal_finance_assistant

run_local_cli_client:
	PYTHONPATH=. uv run clients/cli