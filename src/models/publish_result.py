from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4


class PublishResultStatus(str, Enum):
    """Result status for a published post."""

    PENDING = "pending"
    PUBLISHED = "published"
    FAILED = "failed"
    SCHEDULED = "scheduled"
    DRAFT_ONLY = "draft_only"


@dataclass
class PublishResult:
    """Track the result of publishing a draft variant to a platform."""

    draft_id: str
    variant_id: str
    platform_id: str
    status: PublishResultStatus = PublishResultStatus.PENDING
    result_id: str = field(default_factory=lambda: str(uuid4()))
    published_at: Optional[str] = None
    external_id: Optional[str] = None
    url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def mark_published(self, external_id: str, url: Optional[str] = None) -> None:
        """Mark post as successfully published."""
        self.status = PublishResultStatus.PUBLISHED
        self.external_id = external_id
        self.url = url
        self.published_at = datetime.utcnow().isoformat()

    def mark_failed(self, error_message: str) -> None:
        """Mark post as failed with error details."""
        self.status = PublishResultStatus.FAILED
        self.error_message = error_message

    def mark_scheduled(self) -> None:
        """Mark post as scheduled for later publishing."""
        self.status = PublishResultStatus.SCHEDULED
        self.published_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "draft_id": self.draft_id,
            "variant_id": self.variant_id,
            "platform_id": self.platform_id,
            "status": self.status.value,
            "published_at": self.published_at,
            "external_id": self.external_id,
            "url": self.url,
            "error_message": self.error_message,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }


__all__ = ["PublishResult", "PublishResultStatus"]
