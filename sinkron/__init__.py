"""
Sinkron - Python Library for Sinkron Email API
"""

from .client import SinkronClient
from .config import Config
from .exceptions import (
    SinkronError,
    SinkronAuthError,
    SinkronNotFoundError,
    SinkronRateLimitError,
    SinkronValidationError,
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
    "AgentInfo",
    "Attachment",
    "Message",
    "InboxResponse",
    "RegisterResponse",
    "DeleteMessagesResponse",
    "DeleteInboxResponse",
]
