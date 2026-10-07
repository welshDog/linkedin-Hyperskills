from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .common import PlatformAdapter, PlatformResult, PublishRequest


@dataclass
class DiscordAdapter(PlatformAdapter):
    platform_id: str = "discord"
    display_name: str = "Discord"
    webhook_url: Optional[str] = None

    def publish(self, request: PublishRequest) -> PlatformResult:
        payload = self.build_payload(request)

        if not self.webhook_url:
            return PlatformResult(
                platform_id=self.platform_id,
                status="draft_ready",
                message="Discord webhook not configured. Add a webhook URL to activate live publishing.",
                payload=payload,
            )

        try:
            import httpx

            response = httpx.post(
                self.webhook_url,
                json={
                    "content": request.content,
                    "username": request.metadata.get("bot_name", "Hyperskills Bot"),
                },
                timeout=15,
            )
            response.raise_for_status()
        except Exception as exc:  # pragma: no cover - network and config failure path
            return PlatformResult(
                platform_id=self.platform_id,
                status="failed",
                message=f"Discord publish failed: {exc}",
                payload=payload,
            )

        return PlatformResult(
            platform_id=self.platform_id,
            status="published",
            message="Discord post sent successfully.",
            payload={**payload, "webhook_url": self.webhook_url},
        )


__all__ = ["DiscordAdapter"]
