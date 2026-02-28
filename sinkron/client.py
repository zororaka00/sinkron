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
)
from .models import (
    AgentInfo,
    Attachment,
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
        config_file: Optional[str] = None
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
    
    def _handle_response(self, response: requests.Response):
        """Handle API response and raise appropriate exceptions"""
        status = response.status_code
        
        if status == 200:
            return response.json()
        elif status == 400:
            error = response.json().get("error", "Bad request")
            raise SinkronValidationError(error, status)
        elif status == 401:
            error = response.json().get("error", "Unauthorized")
            raise SinkronAuthError(error, status)
        elif status == 403:
            error = response.json().get("error", "Forbidden")
            raise SinkronAuthError(error, status)
        elif status == 404:
            error = response.json().get("error", "Not found")
            raise SinkronNotFoundError(error, status)
        elif status == 429:
            error = response.json().get("error", "Rate limit exceeded")
            raise SinkronRateLimitError(error, status)
        else:
            error = response.json().get("error", "API error")
            raise SinkronError(error, status)
    
    # ==================== Health ====================
    
    def health_check(self) -> dict:
        """
        Check API health status
        
        Returns:
            dict: Health check response
        """
        url = f"{self.config.api_url}/"
        response = self._session.get(url, headers=self._get_headers())
        return self._handle_response(response)
    
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
        response = self._session.post(url, json=payload, headers=self._get_headers())
        data = self._handle_response(response)
        
        # Auto-save token
        self.config.token = data.get("token")
        
        return RegisterResponse.from_dict(data)
    
    def get_agent_info(self, username: str) -> AgentInfo:
        """
        Get agent information by username
        
        Args:
            username: Username to查询
            
        Returns:
            AgentInfo: Agent information
        """
        if not self.config.token:
            raise SinkronAuthError("Token required. Use 'sinkron config --token' or login first.")
        
        url = f"{self.config.api_url}/agent/{username}"
        response = self._session.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        
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
        
        response = self._session.get(url, params=params, headers=self._get_headers())
        data = self._handle_response(response)
        
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
        response = self._session.delete(url, headers=self._get_headers())
        data = self._handle_response(response)
        
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
        response = self._session.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        
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
        response = self._session.post(url, json=payload, headers=self._get_headers())
        data = self._handle_response(response)
        
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
        response = self._session.get(url, headers=self._get_headers())
        data = self._handle_response(response)
        
        return CheckResponse.from_dict(data)
