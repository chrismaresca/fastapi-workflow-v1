# built-in imports
import json
from typing import List

# pydantic imports
from pydantic import BaseModel


# Types
from .types import ClientAttachment, ToolInvocation, ClientMessage


def convert_to_openai_messages(messages: List[ClientMessage]):
    """
    Convert a list of client messages to a list of OpenAI messages.
    """
    openai_messages = []

    for message in messages:
        parts = []

        parts.append({"type": "text", "text": message.content})

        if message.experimental_attachments:
            for attachment in message.experimental_attachments:
                if attachment.contentType.startswith("image"):
                    parts.append(
                        {"type": "image_url", "image_url": {"url": attachment.url}}
                    )

                elif attachment.contentType.startswith("text"):
                    parts.append({"type": "text", "text": attachment.url})

        if message.toolInvocations:
            tool_calls = [
                {
                    "id": tool_invocation.toolCallId,
                    "type": "function",
                    "function": {
                        "name": tool_invocation.toolName,
                        "arguments": json.dumps(tool_invocation.args),
                    },
                }
                for tool_invocation in message.toolInvocations
            ]

            openai_messages.append({"role": "assistant", "tool_calls": tool_calls})

            tool_results = [
                {
                    "role": "tool",
                    "content": json.dumps(tool_invocation.result),
                    "tool_call_id": tool_invocation.toolCallId,
                }
                for tool_invocation in message.toolInvocations
            ]

            openai_messages.extend(tool_results)

            continue

        openai_messages.append({"role": message.role, "content": parts})

    return openai_messages
