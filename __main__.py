import logging

import click

from dotenv import load_dotenv

from agents.personal_finance_assistant import PersonalFinanceA2AApp


load_dotenv(dotenv_path='./agents/personal_finance_assistant/.env')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=8080)
def main(host, port):
    """Entry point for running the Personal Finance Assistant agent server.

    This function initializes the agent card, request handler, and server
    application, then starts the server using Uvicorn with the specified
    host and port.
    """
    app = PersonalFinanceA2AApp()
    app.start(host, port)


if __name__ == '__main__':
    main()
