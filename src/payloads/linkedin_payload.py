from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.models import Variant


class LinkedInPostPayloadBuilder:
    """Builds a LinkedIn-ready publishing payload from a Hyperskills draft."""

    def __init__(self, variant: Variant, founder_profile: Optional[Dict[str, Any]] = None):
        self.variant = variant
        self.founder_profile = founder_profile or {}

    def build(self) -> Dict[str, Any]:
        """
        Build a LinkedIn post payload.
        This is a skeleton that can be extended with actual LinkedIn API bindings.
        """
        return {
            "text": self.variant.content,
            "visibility": self._visibility(),
            "commentary": self._commentary(),
            "content": self._content_metadata(),
            "distribution": self._distribution(),
        }

    def _visibility(self) -> Dict[str, str]:
        """Default to public visibility."""
        return {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}

    def _commentary(self) -> str:
        """Return the variant content as commentary."""
        return self.variant.content

    def _content_metadata(self) -> Dict[str, Any]:
        """Extract content metadata if available."""
        return {
            "variant_id": self.variant.variant_id,
            "score": self.variant.score,
            "claim_risk": self.variant.claim_risk,
        }

    def _distribution(self) -> Dict[str, Any]:
        """Distribution settings for the post."""
        return {
            "feed_distribution": "MAIN_FEED",
            "targeted_editing_on_creation": False,
        }

    def to_json(self) -> Dict[str, Any]:
        """Serialize to JSON for API submission."""
        return self.build()


__all__ = ["LinkedInPostPayloadBuilder"]
