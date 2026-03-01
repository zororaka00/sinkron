"""
Data models for Sinkron API
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Attachment:
    """Attachment model"""

    filename: str
    mime_type: str
    size: int
    download_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            filename=data.get("filename", ""),
            mime_type=data.get("mime_type", ""),
            size=data.get("size", 0),
            download_url=data.get("download_url"),
        )


@dataclass
class Message:
    """Message model"""

    id: int
    agent_id: int
    from_address: str
    subject: str
    body: str
    received_at: str
    attachments: List[Attachment] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        attachments = []
        if data.get("attachments"):
            attachments = [Attachment.from_dict(a) for a in data["attachments"]]
        return cls(
            id=data.get("id", 0),
            agent_id=data.get("agent_id", 0),
            from_address=data.get("from_address", ""),
            subject=data.get("subject", ""),
            body=data.get("body", ""),
            received_at=data.get("received_at", ""),
            attachments=attachments,
        )

    def format_display(self) -> str:
        """Format message for display"""
        lines = [
            f"ID: {self.id}",
            f"From: {self.from_address}",
            f"Subject: {self.subject}",
            f"Received: {self.received_at}",
            f"Attachments: {len(self.attachments)}",
        ]
        if self.attachments:
            lines.append("\nAttachments:")
            for att in self.attachments:
                lines.append(f"  - {att.filename} ({att.mime_type}, {att.size} bytes)")
        lines.append(f"\nBody:\n{self.body}")
        return "\n".join(lines)


@dataclass
class AgentInfo:
    """Agent information model"""

    id: int
    username: str
    name: str
    address: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id", 0),
            username=data.get("username", ""),
            name=data.get("name", ""),
            address=data.get("address", ""),
            created_at=data.get("created_at", ""),
        )

    def format_display(self) -> str:
        """Format agent info for display"""
        return (
            f"ID: {self.id}\n"
            f"Username: {self.username}\n"
            f"Name: {self.name}\n"
            f"Email Address: {self.address}\n"
            f"Created: {self.created_at}"
        )


@dataclass
class RegisterResponse:
    """Registration response model"""

    username: str
    token: str
    address: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            username=data.get("username", ""),
            token=data.get("token", ""),
            address=data.get("address", ""),
            created_at=data.get("created_at", ""),
        )


@dataclass
class Pagination:
    """Pagination info"""

    page: int
    limit: int
    total_items: int
    total_pages: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            page=data.get("page", 1),
            limit=data.get("limit", 25),
            total_items=data.get("total_items", 0),
            total_pages=data.get("total_pages", 1),
        )


@dataclass
class InboxResponse:
    """Inbox response model"""

    address: str
    pagination: Pagination
    messages: List[Message]

    @classmethod
    def from_dict(cls, data: dict):
        messages = []
        if data.get("messages"):
            messages = [Message.from_dict(m) for m in data["messages"]]

        pagination_data = data.get("pagination", {})
        pagination = Pagination.from_dict(pagination_data)

        return cls(address=data.get("address", ""), pagination=pagination, messages=messages)

    def format_display(self) -> str:
        """Format inbox for display"""
        lines = [
            f"Inbox: {self.address}",
            (
                f"Page {self.pagination.page} of {self.pagination.total_pages}"
                f" (Total: {self.pagination.total_items} messages)"
            ),
            "=" * 60,
        ]
        for msg in self.messages:
            att_count = len(msg.attachments)
            att_info = (
                f" [{att_count} attachment{'s' if att_count != 1 else ''}]" if att_count > 0 else ""
            )
            lines.append(
                f"[{msg.id}] {msg.from_address}\n"
                f"     Subject: {msg.subject[:50]}{'...' if len(msg.subject) > 50 else ''}"
                f"{att_info}"
            )
        return "\n".join(lines)


@dataclass
class DeleteMessagesResponse:
    """Delete messages response model"""

    success: bool
    deleted: int
    errors: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            success=data.get("success", False),
            deleted=data.get("deleted", 0),
            errors=data.get("errors", []),
        )

    def format_display(self) -> str:
        """Format delete response for display"""
        lines = [
            f"Success: {self.success}",
            f"Deleted: {self.deleted} message(s)",
        ]
        if self.errors:
            lines.append("Errors:")
            for err in self.errors:
                lines.append(f"  - {err}")
        return "\n".join(lines)


@dataclass
class DeleteInboxResponse:
    """Delete inbox response model"""

    success: bool
    message: str
    errors: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            success=data.get("success", False),
            message=data.get("message", ""),
            errors=data.get("errors", []),
        )

    def format_display(self) -> str:
        """Format delete inbox response for display"""
        lines = [
            f"Success: {self.success}",
            f"Message: {self.message}",
        ]
        if self.errors:
            lines.append("Errors:")
            for err in self.errors:
                lines.append(f"  - {err}")
        return "\n".join(lines)


@dataclass
class CheckResponse:
    """Check email response model"""

    address: str
    exists: bool

    @classmethod
    def from_dict(cls, data: dict):
        return cls(address=data.get("address", ""), exists=data.get("exists", False))

    def format_display(self) -> str:
        """Format check response for display"""
        status = "Registered" if self.exists else "Not Registered"
        return f"{self.address}: {status}"
