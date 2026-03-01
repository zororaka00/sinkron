"""Tests for sinkron models"""
import pytest
from sinkron.models import (
    AgentInfo,
    Attachment,
    Message,
    InboxResponse,
    RegisterResponse,
    DeleteMessagesResponse,
    DeleteInboxResponse,
    CheckResponse,
    Pagination,
)


class TestAttachment:
    """Tests for Attachment model"""

    def test_from_dict(self):
        """Test creating Attachment from dict"""
        data = {
            "filename": "test.txt",
            "mime_type": "text/plain",
            "size": 1024,
            "download_url": "https://example.com/file",
        }
        att = Attachment.from_dict(data)
        assert att.filename == "test.txt"
        assert att.mime_type == "text/plain"
        assert att.size == 1024
        assert att.download_url == "https://example.com/file"

    def test_from_dict_with_defaults(self):
        """Test creating Attachment with missing fields"""
        data = {}
        att = Attachment.from_dict(data)
        assert att.filename == ""
        assert att.mime_type == ""
        assert att.size == 0
        assert att.download_url is None


class TestMessage:
    """Tests for Message model"""

    def test_from_dict(self):
        """Test creating Message from dict"""
        data = {
            "id": 1,
            "agent_id": 10,
            "from_address": "sender@example.com",
            "subject": "Test Subject",
            "body": "Test body content",
            "received_at": "2024-01-01T00:00:00Z",
            "attachments": [],
        }
        msg = Message.from_dict(data)
        assert msg.id == 1
        assert msg.agent_id == 10
        assert msg.from_address == "sender@example.com"
        assert msg.subject == "Test Subject"
        assert msg.body == "Test body content"
        assert msg.received_at == "2024-01-01T00:00:00Z"
        assert msg.attachments == []

    def test_from_dict_with_attachments(self):
        """Test creating Message with attachments"""
        data = {
            "id": 1,
            "agent_id": 10,
            "from_address": "sender@example.com",
            "subject": "Test Subject",
            "body": "Test body",
            "received_at": "2024-01-01T00:00:00Z",
            "attachments": [
                {
                    "filename": "test.txt",
                    "mime_type": "text/plain",
                    "size": 1024,
                    "download_url": "https://example.com/file",
                }
            ],
        }
        msg = Message.from_dict(data)
        assert len(msg.attachments) == 1
        assert msg.attachments[0].filename == "test.txt"


class TestAgentInfo:
    """Tests for AgentInfo model"""

    def test_from_dict(self):
        """Test creating AgentInfo from dict"""
        data = {
            "id": 1,
            "username": "testuser",
            "name": "Test User",
            "address": "testuser@sinkron.id",
            "created_at": "2024-01-01T00:00:00Z",
        }
        agent = AgentInfo.from_dict(data)
        assert agent.id == 1
        assert agent.username == "testuser"
        assert agent.name == "Test User"
        assert agent.address == "testuser@sinkron.id"
        assert agent.created_at == "2024-01-01T00:00:00Z"


class TestRegisterResponse:
    """Tests for RegisterResponse model"""

    def test_from_dict(self):
        """Test creating RegisterResponse from dict"""
        data = {
            "username": "testuser",
            "token": "test_token_123",
            "address": "testuser@sinkron.id",
            "created_at": "2024-01-01T00:00:00Z",
        }
        resp = RegisterResponse.from_dict(data)
        assert resp.username == "testuser"
        assert resp.token == "test_token_123"
        assert resp.address == "testuser@sinkron.id"
        assert resp.created_at == "2024-01-01T00:00:00Z"


class TestPagination:
    """Tests for Pagination model"""

    def test_from_dict(self):
        """Test creating Pagination from dict"""
        data = {
            "page": 1,
            "limit": 25,
            "total_items": 100,
            "total_pages": 4,
        }
        pagination = Pagination.from_dict(data)
        assert pagination.page == 1
        assert pagination.limit == 25
        assert pagination.total_items == 100
        assert pagination.total_pages == 4

    def test_from_dict_with_defaults(self):
        """Test creating Pagination with defaults"""
        data = {}
        pagination = Pagination.from_dict(data)
        assert pagination.page == 1
        assert pagination.limit == 25
        assert pagination.total_items == 0
        assert pagination.total_pages == 1


class TestInboxResponse:
    """Tests for InboxResponse model"""

    def test_from_dict(self):
        """Test creating InboxResponse from dict"""
        data = {
            "address": "testuser@sinkron.id",
            "pagination": {
                "page": 1,
                "limit": 25,
                "total_items": 100,
                "total_pages": 4,
            },
            "messages": [],
        }
        resp = InboxResponse.from_dict(data)
        assert resp.address == "testuser@sinkron.id"
        assert resp.pagination.page == 1
        assert resp.pagination.total_items == 100
        assert resp.messages == []


class TestDeleteMessagesResponse:
    """Tests for DeleteMessagesResponse model"""

    def test_from_dict(self):
        """Test creating DeleteMessagesResponse from dict"""
        data = {"success": True, "deleted": 5, "errors": []}
        resp = DeleteMessagesResponse.from_dict(data)
        assert resp.success is True
        assert resp.deleted == 5
        assert resp.errors == []

    def test_from_dict_with_errors(self):
        """Test creating with errors"""
        data = {"success": False, "deleted": 3, "errors": ["Error 1", "Error 2"]}
        resp = DeleteMessagesResponse.from_dict(data)
        assert resp.success is False
        assert resp.deleted == 3
        assert len(resp.errors) == 2


class TestDeleteInboxResponse:
    """Tests for DeleteInboxResponse model"""

    def test_from_dict(self):
        """Test creating DeleteInboxResponse from dict"""
        data = {"success": True, "message": "Inbox deleted", "errors": []}
        resp = DeleteInboxResponse.from_dict(data)
        assert resp.success is True
        assert resp.message == "Inbox deleted"
        assert resp.errors == []


class TestCheckResponse:
    """Tests for CheckResponse model"""

    def test_from_dict_exists(self):
        """Test creating CheckResponse when email exists"""
        data = {"address": "test@sinkron.id", "exists": True}
        resp = CheckResponse.from_dict(data)
        assert resp.address == "test@sinkron.id"
        assert resp.exists is True

    def test_from_dict_not_exists(self):
        """Test creating CheckResponse when email doesn't exist"""
        data = {"address": "test@sinkron.id", "exists": False}
        resp = CheckResponse.from_dict(data)
        assert resp.address == "test@sinkron.id"
        assert resp.exists is False
