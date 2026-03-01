"""
Sinkron - Python Library for Permanent Email for AI Agents
Give your agent permanent email addresses through Clawhub.
"""

from .client import SinkronClient
from .config import Config
from .exceptions import (
    SinkronError,
    SinkronAuthError,
    SinkronNotFoundError,
    SinkronRateLimitError,
    SinkronValidationError,
    SinkronAPIError,
    SinkronConnectionError,
)
from .models import (
    AgentInfo,
    Attachment,
    Message,
    InboxResponse,
    RegisterResponse,
    DeleteMessagesResponse,
    DeleteInboxResponse,
)

__version__ = "1.0.0"
__all__ = [
    "SinkronClient",
    "Config",
    "SinkronError",
    "SinkronAuthError",
    "SinkronNotFoundError",
    "SinkronRateLimitError",
    "SinkronValidationError",
    "SinkronAPIError",
    "SinkronConnectionError",
    "AgentInfo",
    "Attachment",
    "Message",
    "InboxResponse",
    "RegisterResponse",
    "DeleteMessagesResponse",
    "DeleteInboxResponse",
]
