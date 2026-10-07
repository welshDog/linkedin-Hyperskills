from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class DraftStatus(str, Enum):
    """Founder draft workflow state machine."""

    CREATED = "created"
    SCORING = "scoring"
    SCORED = "scored"
    SAFETY_CHECK = "safety_check"
    FLAGGED = "flagged"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"


@dataclass
class Variant:
    """A single draft variant for scoring and approval."""

    content: str
    variant_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    score: Optional[float] = None
    claim_risk: Optional[str] = None
    approved: bool = False
    approved_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "variant_id": self.variant_id,
            "content": self.content,
            "score": self.score,
            "claim_risk": self.claim_risk,
            "approved": self.approved,
            "approved_at": self.approved_at,
            "created_at": self.created_at,
        }


@dataclass
class Draft:
    """A founder's draft post with multiple variants and approval workflow."""

    founder_id: str
    title: str
    brief: str
    platforms: List[str] = field(default_factory=list)
    variants: List[Variant] = field(default_factory=list)
    status: DraftStatus = DraftStatus.CREATED
    draft_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: List[str] = field(default_factory=list)
    scheduled_for: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_variant(self, content: str) -> Variant:
        """Create and add a new draft variant."""
        variant = Variant(content=content)
        self.variants.append(variant)
        self.updated_at = datetime.utcnow().isoformat()
        return variant

    def set_status(self, status: DraftStatus) -> None:
        """Transition draft to a new status."""
        self.status = status
        self.updated_at = datetime.utcnow().isoformat()

    def approve_variant(self, variant_id: str) -> bool:
        """Mark a variant as approved."""
        for variant in self.variants:
            if variant.variant_id == variant_id:
                variant.approved = True
                variant.approved_at = datetime.utcnow().isoformat()
                self.set_status(DraftStatus.APPROVED)
                return True
        return False

    def reject_variant(self, variant_id: str) -> bool:
        """Mark a variant as rejected."""
        for variant in self.variants:
            if variant.variant_id == variant_id:
                self.set_status(DraftStatus.REJECTED)
                return True
        return False

    def get_approved_variant(self) -> Optional[Variant]:
        """Get the approved variant for publishing."""
        for variant in self.variants:
            if variant.approved:
                return variant
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "draft_id": self.draft_id,
            "founder_id": self.founder_id,
            "title": self.title,
            "brief": self.brief,
            "platforms": self.platforms,
            "status": self.status.value,
            "variants": [v.to_dict() for v in self.variants],
            "tags": self.tags,
            "scheduled_for": self.scheduled_for,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }


__all__ = ["Draft", "DraftStatus", "Variant"]
