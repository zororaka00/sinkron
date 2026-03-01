"""
Main client for Sinkron API
"""

import requests
from typing import Optional, List
from .config import Config
from .exceptions import (
    SinkronError,
    SinkronAuthError,
    SinkronNotFoundError,
    SinkronRateLimitError,
    SinkronValidationError,
    SinkronAPIError,
)
from .models import (
    AgentInfo,
    Message,
    InboxResponse,
    RegisterResponse,
    DeleteMessagesResponse,
    DeleteInboxResponse,
    CheckResponse,
)


class SinkronClient:
    """Main client for interacting with Sinkron API"""

    def __init__(
        self,
        token: Optional[str] = None,
        api_url: Optional[str] = None,
        config_file: Optional[str] = None,
    ):
        """
        Initialize Sinkron client

        Args:
            token: Authentication token
            api_url: API base URL
            config_file: Path to config file
        """
        self.config = Config(api_url=api_url, token=token, config_file=config_file)
        self._session = requests.Session()

    @property
    def token(self) -> Optional[str]:
        """Get current token"""
        return self.config.token

    @token.setter
    def token(self, value: str):
        """Set authentication token"""
        self.config.token = value

    def _get_headers(self) -> dict:
        """Get request headers"""
        headers = {"Content-Type": "application/json"}
        if self.config.token:
            headers["Authorization"] = f"Bearer {self.config.token}"
        return headers

    def _make_request(self, method: str, url: str, **kwargs):
        """Make HTTP request with error handling"""
        try:
            response = self._session.request(method, url, **kwargs)
        except requests.exceptions.ConnectionError:
            raise SinkronError(
                f"Cannot connect to API at {self.config.api_url}. "
                f"Make sure the server is running or check the API URL. "
                f"Use '--api-url http://localhost:8787' for local development."
            )
        except requests.exceptions.Timeout:
            raise SinkronError("Connection timed out. Please try again.")
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response):
        """Handle API response and raise appropriate exceptions"""
        status = response.status_code

        # Try to parse error response
        try:
            error_data = response.json()
            error = error_data.get("error", "Unknown error")
        except Exception:
            error = response.text or "Unknown error"

        if status == 200:
            return response.json()
        elif status == 400:
            raise SinkronValidationError(error, status)
        elif status == 401:
            raise SinkronAuthError(error, status)
        elif status == 403:
            raise SinkronAuthError(error, status)
        elif status == 404:
            raise SinkronNotFoundError(error, status)
        elif status == 429:
            raise SinkronRateLimitError(error, status)
        else:
            raise SinkronAPIError(error, status)

    # ==================== Health ====================

    def health_check(self) -> dict:
        """
        Check API health status

        Returns:
            dict: Health check response
        """
        url = f"{self.config.api_url}/"
        return self._make_request("GET", url)

    # ==================== Agent ====================

    def register(self, username: str, name: str) -> RegisterResponse:
        """
        Register a new agent

        Args:
            username: Username (4-25 lowercase alphanumeric)
            name: Display name

        Returns:
            RegisterResponse: Registration response with token
        """
        # Validate username
        if not username or len(username) < 4 or len(username) > 25:
            raise SinkronValidationError("Username must be 4-25 characters")
        if not username.islower() or not username.isalnum():
            raise SinkronValidationError("Username must be lowercase alphanumeric")
        if not name or len(name) < 1:
            raise SinkronValidationError("Name is required")

        url = f"{self.config.api_url}/register"
        payload = {"username": username, "name": name}
        data = self._make_request("POST", url, json=payload)

        # Auto-save token
        self.config.token = data.get("token")

        return RegisterResponse.from_dict(data)

    def get_agent_info(self, username: str) -> AgentInfo:
        """
        Get agent information by username

        Args:
            username: Username to query

        Returns:
            AgentInfo: Agent information
        """
        if not self.config.token:
            raise SinkronAuthError("Token required. Use 'sinkron config --token' or login first.")

        url = f"{self.config.api_url}/agent/{username}"
        data = self._make_request("GET", url)

        return AgentInfo.from_dict(data)

    # ==================== Inbox ====================

    def get_inbox(self, page: int = 1, search: str = None) -> InboxResponse:
        """
        Get paginated inbox messages

        Args:
            page: Page number (default: 1)
            search: Search keyword

        Returns:
            InboxResponse: Paginated inbox messages
        """
        if not self.config.token:
            raise SinkronAuthError("Token required. Use 'sinkron config --token' or login first.")

        url = f"{self.config.api_url}/inbox"
        params = {"page": str(page)}
        if search:
            params["search"] = search

        data = self._make_request("GET", url, params=params)

        return InboxResponse.from_dict(data)

    def delete_inbox(self) -> DeleteInboxResponse:
        """
        Delete entire inbox and all messages

        Returns:
            DeleteInboxResponse: Delete result
        """
        if not self.config.token:
            raise SinkronAuthError("Token required. Use 'sinkron config --token' or login first.")

        url = f"{self.config.api_url}/inbox/delete"
        data = self._make_request("POST", url)

        return DeleteInboxResponse.from_dict(data)

    # ==================== Messages ====================

    def get_message(self, message_id: int) -> Message:
        """
        Get a single message by ID

        Args:
            message_id: Message ID

        Returns:
            Message: Message details
        """
        if not self.config.token:
            raise SinkronAuthError("Token required. Use 'sinkron config --token' or login first.")

        url = f"{self.config.api_url}/message/{message_id}"
        data = self._make_request("GET", url)

        return Message.from_dict(data)

    def delete_messages(self, message_ids: List[int]) -> DeleteMessagesResponse:
        """
        Batch delete messages

        Args:
            message_ids: List of message IDs to delete (max 25)

        Returns:
            DeleteMessagesResponse: Delete result
        """
        if not self.config.token:
            raise SinkronAuthError("Token required. Use 'sinkron config --token' or login first.")

        if not message_ids or len(message_ids) == 0:
            raise SinkronValidationError("At least one message ID required")

        if len(message_ids) > 25:
            raise SinkronValidationError("Maximum 25 messages can be deleted at once")

        url = f"{self.config.api_url}/messages/delete"
        payload = {"ids": message_ids}
        data = self._make_request("POST", url, json=payload)

        return DeleteMessagesResponse.from_dict(data)

    # ==================== Check ====================

    def check_email(self, address: str) -> CheckResponse:
        """
        Check if email address exists

        Args:
            address: Email address to check

        Returns:
            CheckResponse: Check result
        """
        url = f"{self.config.api_url}/check/{address}"
        data = self._make_request("GET", url)

        return CheckResponse.from_dict(data)
