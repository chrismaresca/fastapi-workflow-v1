from pydantic import BaseModel
from typing import List, Optional


class ClientMessage(BaseModel):
    """
    A message from the client to the server.
    """
    role: str
    content: str
    experimental_attachments: Optional[List["ClientAttachment"]] = None
    toolInvocations: Optional[List["ToolInvocation"]] = None


class ClientAttachment(BaseModel):
    """
    An attachment from the client to the server.
    """
    name: str
    contentType: str
    url: str


class ToolInvocation(BaseModel):
    """
    A tool invocation from the client to the server.
    """
    toolCallId: str
    toolName: str
    args: dict
    result: dict
