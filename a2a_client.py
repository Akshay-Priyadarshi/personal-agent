#!/usr/bin/env python3
"""a2a_client.py — Interactive A2A chat client."""

import asyncio
import logging
import traceback

from uuid import uuid4

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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('a2a_client')


async def chat():
    """Starts an interactive chat session with the A2A agent.
    Connects to the agent server, sends user input as messages, and displays
    agent responses.
    Type '/exit' to quit the chat.
    """
    server_url = 'http://127.0.0.1:8080/'
    async with (
        httpx.AsyncClient(timeout=30) as agent_httpx_client,
    ):
        agent_a2a_client = A2AClient(
            url=server_url, httpx_client=agent_httpx_client
        )
        agent_card_resolver = A2ACardResolver(
            httpx_client=agent_httpx_client, base_url=server_url
        )
        agent_card = await agent_card_resolver.get_agent_card()

        typer.clear()
        logger.info(
            f"""Connected to agent at {server_url}
Agent Card: {agent_card.model_dump_json(indent=2)}
Type '/exit' to quit.
        """
        )
        while True:
            user_input = typer.prompt('\nUser 🧑')
            if user_input.strip().lower() == '/exit':
                logger.info('Exiting chat.')
                break
            message = Message(
                messageId=str(uuid4()),
                role=Role.user,
                parts=[TextPart(text=user_input)],
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
                # logger.info the full JSON for debugging
                logger.info(f'Agent: {response.model_dump_json()}')
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
                        typer.echo(f'\nAgent 🤖: {content}')
                    else:
                        logger.info("No 'response' artifact found.")
                except Exception as e:
                    logger.error(
                        f'Error extracting agent response text: {e}\n{
                            traceback.format_exc()
                        }'
                    )
            except Exception as e:
                logger.error(f'Error: {e}\n{traceback.format_exc()}')


if __name__ == '__main__':
    typer.run(asyncio.run(chat()))
