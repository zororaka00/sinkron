"""
Custom exceptions for Sinkron API
"""


class SinkronError(Exception):
    """Base exception for all Sinkron API errors"""

    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class SinkronAuthError(SinkronError):
    """Authentication error - invalid or missing token"""

    pass


class SinkronNotFoundError(SinkronError):
    """Resource not found"""

    pass


class SinkronRateLimitError(SinkronError):
    """Rate limit exceeded"""

    pass


class SinkronValidationError(SinkronError):
    """Validation error - invalid input"""

    pass


class SinkronAPIError(SinkronError):
    """General API error"""

    pass


class SinkronConnectionError(SinkronError):
    """Connection error - cannot reach API server"""

    pass
