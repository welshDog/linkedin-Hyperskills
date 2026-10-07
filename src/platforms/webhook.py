from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .common import PlatformAdapter, PlatformResult, PublishRequest


@dataclass
class WebhookAdapter(PlatformAdapter):
    platform_id: str = "webhook"
    display_name: str = "Generic Webhook"
    endpoint_url: Optional[str] = None
    auth_token: Optional[str] = None

    def publish(self, request: PublishRequest) -> PlatformResult:
        payload = self.build_payload(request)

        if not self.endpoint_url:
            return PlatformResult(
                platform_id=self.platform_id,
                status="draft_ready",
                message="Webhook endpoint not configured yet.",
                payload=payload,
            )

        try:
            import httpx

            headers = {"Content-Type": "application/json"}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"

            response = httpx.post(
                self.endpoint_url,
                json={
                    "title": request.title,
                    "content": request.content,
                    "tags": request.tags,
                    "platform_ids": request.platform_ids,
                    "metadata": request.metadata,
                },
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()
        except Exception as exc:  # pragma: no cover - network and config failure path
            return PlatformResult(
                platform_id=self.platform_id,
                status="failed",
                message=f"Generic webhook publish failed: {exc}",
                payload=payload,
            )

        return PlatformResult(
            platform_id=self.platform_id,
            status="published",
            message="Webhook call succeeded.",
            payload={**payload, "endpoint_url": self.endpoint_url},
        )


__all__ = ["WebhookAdapter"]
