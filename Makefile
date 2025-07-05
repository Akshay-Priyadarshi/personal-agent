setup:
	bash setup.bash

run_adk_web:
	PYTHONPATH=. adk web ./agents

run_local_personal_finance_assistant:
	APP_ENV=development PYTHONPATH=. uv run agents/personal_finance_assistant

run_cli_client:
	uv run clients/cli