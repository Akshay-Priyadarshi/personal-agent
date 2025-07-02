setup:
	bash setup.bash

run_adk_web:
	PYTHONPATH=. adk web ./agents

run_a2a_server:
	uv run __main__.py

run_a2a_client:
	uv run a2a_client.py