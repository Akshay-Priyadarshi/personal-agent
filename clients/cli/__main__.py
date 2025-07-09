#!/usr/bin/env python3
"""__main__.py — Interactive A2A CLI chat client."""

# imports
import asyncio
import os

from uuid import uuid4

import dotenv
import httpx
import typer

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    Message,
    MessageSendParams,
    Role,
    SendMessageRequest,
    TextPart,
)

from utils import EnvironmentUtils, LoggerUtils


# configure environment varables
dotenv.load_dotenv(dotenv.find_dotenv())

# configure logging
logger = LoggerUtils.get_logger(
    __name__,
    level=LoggerUtils.LogLevel(
        int(EnvironmentUtils.read_env_var('APP_LOG_LEVEL'))
    ),
    file_path='./clients/cli/cli_client.log',
)


async def chat(
    agent_url: str = typer.Option(
        'http://127.0.0.1:8080/',
        envvar='AGENT_A2A_URL',
        help='Agent A2A URL',
    ),
):
    """Starts an interactive chat session with the A2A agent.
    Connects to the agent server, sends user input as messages, and displays
    agent responses.
    Type '/exit' to quit the chat.
    """
    async with (
        httpx.AsyncClient(timeout=30) as agent_httpx_client,
    ):
        agent_a2a_client = A2AClient(
            url=agent_url, httpx_client=agent_httpx_client
        )
        agent_card_resolver = A2ACardResolver(
            httpx_client=agent_httpx_client, base_url=agent_url
        )
        try:
            agent_card = await agent_card_resolver.get_agent_card()
        except Exception as e:
            logger.exception(e)
            raise e

        logger.debug(
            f"""Connected to agent at {agent_url}
Type '/exit' to quit.
        """,
            extra={'agent_card': agent_card.model_dump()},
        )
        while True:
            user_input = input('\nUser 🧑: ')
            if user_input.strip().lower() == '/exit':
                logger.info('Exiting chat.')
                break
            message = Message(
                messageId=str(uuid4()),
                role=Role.user,
                parts=[TextPart(text=user_input)],
                contextId='8e81653c-bf14-486c-8374-6cb024448d35',
            )
            try:
                response = await agent_a2a_client.send_message(
                    request=SendMessageRequest(
                        id=str(uuid4()),
                        params=MessageSendParams(
                            message=message,
                        ),
                    )
                )
                # logger.debug the full JSON for debugging
                logger.debug(
                    'agent response received',
                    extra={'agent_response': response.model_dump()},
                )
                # Try to extract the text from the response artifacts
                try:
                    # Access artifacts from the response
                    artifacts = (
                        response.root.result.artifacts
                    )  # Adjust this path if needed
                    # Find the artifact named "response"
                    artifact = next(
                        (a for a in artifacts if a.name == 'response'), None
                    )
                    if artifact:
                        parts = artifact.parts
                        # Try both dict and attribute access for 'text'
                        content = ''
                        for part in parts:
                            if isinstance(part, dict):
                                content += part.get('text', '')
                            else:
                                content += part.root.text
                        logger.debug(
                            'successfully extracted agent reply',
                            extra={'agent_reply': content},
                        )
                        print('\nAgent 🤖: ', content)
                    else:
                        logger.warn("No 'response' artifact found.")
                except Exception as e:
                    logger.exception(e)
                    raise e
            except Exception as e:
                logger.exception(e)
                raise e


# run the chat function
if __name__ == '__main__':
    typer.run(
        asyncio.run(
            chat(agent_url=EnvironmentUtils.read_env_var('AGENT_A2A_URL'))
        )
    )
