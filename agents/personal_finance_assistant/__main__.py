# imports
import logging
import os

import click

from dotenv import load_dotenv

from agents.personal_finance_assistant.a2a_app import PersonalFinanceA2AApp


# cofigure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

# configure app environment
APP_ENV = os.getenv('APP_ENV')

if APP_ENV == 'development':
    load_dotenv(dotenv_path='./agents/personal_finance_assistant/.env')


# setup main function
@click.command()
@click.option(
    '--host', envvar='APP_HOST', default='0.0.0.0', help='Host address'
)
@click.option(
    '--port', envvar='APP_PORT', default=8080, type=int, help='Port number'
)
def main(host: str, port: int):
    """Entry point for running the Personal Finance Assistant A2A server.

    This function initializes the agent card, request handler, and server
    application, then starts the server using Uvicorn with the specified
    host and port.
    """
    app = PersonalFinanceA2AApp()
    app.start(host, port)


# run the main function
if __name__ == '__main__':
    main()
