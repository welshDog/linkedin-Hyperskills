from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .common import PlatformAdapter, PlatformResult, PublishRequest


@dataclass
class LinkedInAdapter(PlatformAdapter):
    platform_id: str = "linkedin"
    display_name: str = "LinkedIn"
    api_base_url: Optional[str] = None
    access_token: Optional[str] = None

    def build_payload(self, request: PublishRequest) -> Dict[str, Any]:
        payload = super().build_payload(request)
        payload["author_profile"] = request.metadata.get("author_profile", "founder")
        return payload

    def publish(self, request: PublishRequest) -> PlatformResult:
        payload = self.build_payload(request)

        if not self.api_base_url or not self.access_token:
            return PlatformResult(
                platform_id=self.platform_id,
                status="draft_ready",
                message="LinkedIn adapter is ready for integration. Add API credentials to enable live publishing.",
                payload=payload,
            )

        try:
            import httpx

            response = httpx.post(
                f"{self.api_base_url.rstrip('/')}/posts",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "text": request.content,
                    "title": request.title,
                    "tags": request.tags,
                    "scheduled_for": request.scheduled_for,
                },
                timeout=20,
            )
            response.raise_for_status()
        except Exception as exc:  # pragma: no cover - network and config failure path
            return PlatformResult(
                platform_id=self.platform_id,
                status="failed",
                message=f"LinkedIn publish failed: {exc}",
                payload=payload,
            )

        return PlatformResult(
            platform_id=self.platform_id,
            status="published",
            message="LinkedIn post queued successfully.",
            payload={**payload, "api_base_url": self.api_base_url},
        )


__all__ = ["LinkedInAdapter"]
