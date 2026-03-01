"""
Configuration management for Sinkron API
"""
import os
from pathlib import Path
from typing import Optional
import json


class Config:
    """Configuration class for Sinkron API"""
    
    DEFAULT_API_URL = "https://api.sinkron.id"
    DEFAULT_CONFIG_FILE = ".sinkron.json"
    
    def __init__(
        self,
        api_url: Optional[str] = None,
        token: Optional[str] = None,
        config_file: Optional[str] = None
    ):
        """
        Initialize configuration
        
        Args:
            api_url: API base URL (default: https://api.sinkron.id)
            token: Authentication token
            config_file: Path to config file
        """
        self._api_url = api_url or self.DEFAULT_API_URL
        self._token = token
        self._config_file = config_file or self.DEFAULT_CONFIG_FILE
        
        # Load from environment variables
        self._load_from_env()
        
        # Load from config file if exists
        self._load_from_file()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        if os.getenv("SINKRON_API_URL"):
            self._api_url = os.getenv("SINKRON_API_URL")
        if os.getenv("SINKRON_TOKEN"):
            self._token = os.getenv("SINKRON_TOKEN")
    
    def _load_from_file(self):
        """Load configuration from file"""
        config_path = Path.home() / self._config_file
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    if not self._token and data.get("token"):
                        self._token = data.get("token")
                    if data.get("api_url"):
                        self._api_url = data.get("api_url")
            except (json.JSONDecodeError, IOError):
                pass
    
    def save(self, config_file: Optional[str] = None):
        """Save configuration to file"""
        config_path = Path.home() / (config_file or self._config_file)
        data = {
            "api_url": self._api_url,
        }
        if self._token:
            data["token"] = self._token
        
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @property
    def api_url(self) -> str:
        """Get API URL"""
        return self._api_url
    
    @api_url.setter
    def api_url(self, value: str):
        """Set API URL"""
        self._api_url = value
    
    @property
    def token(self) -> Optional[str]:
        """Get authentication token"""
        return self._token
    
    @token.setter
    def token(self, value: str):
        """Set authentication token"""
        self._token = value
    
    def clear_token(self):
        """Clear saved token"""
        self._token = None
