"""Real platform adapter implementations."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from src.platforms import PlatformAdapter, PlatformResult, PublishRequest


class RealLinkedInAdapter(PlatformAdapter):
    """Real LinkedIn API adapter (requires credentials)."""

    platform_id: str = "linkedin"
    display_name: str = "LinkedIn"

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.api_base_url = "https://api.linkedin.com/v2"

    def publish(self, request: PublishRequest) -> PlatformResult:
        if not self.access_token:
            return PlatformResult(
                platform_id=self.platform_id,
                status="draft_ready",
                message="LinkedIn access token not configured.",
                payload=self.build_payload(request),
            )

        try:
            import httpx

            # Build LinkedIn-specific payload
            linkedin_payload = {
                "commentary": {"text": request.content},
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            }

            if request.metadata.get("scheduled_for"):
                linkedin_payload["lifecycleState"] = "PENDING"
                linkedin_payload["postPublishTime"] = request.metadata.get(
                    "scheduled_for"
                )

            response = httpx.post(
                f"{self.api_base_url}/ugcPosts",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                },
                json=linkedin_payload,
                timeout=30,
            )

            if response.status_code in [200, 201]:
                post_id = response.headers.get("x-linkedin-id", "unknown")
                return PlatformResult(
                    platform_id=self.platform_id,
                    status="published",
                    message="Post published to LinkedIn",
                    payload={
                        **self.build_payload(request),
                        "post_id": post_id,
                        "post_url": f"https://www.linkedin.com/feed/update/{post_id}",
                    },
                )
            else:
                return PlatformResult(
                    platform_id=self.platform_id,
                    status="failed",
                    message=f"LinkedIn API error: {response.status_code}",
                    payload=self.build_payload(request),
                )
        except Exception as e:
            return PlatformResult(
                platform_id=self.platform_id,
                status="failed",
                message=f"LinkedIn publish failed: {str(e)}",
                payload=self.build_payload(request),
            )


class RealDiscordAdapter(PlatformAdapter):
    """Real Discord webhook adapter."""

    platform_id: str = "discord"
    display_name: str = "Discord"

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")

    def publish(self, request: PublishRequest) -> PlatformResult:
        if not self.webhook_url:
            return PlatformResult(
                platform_id=self.platform_id,
                status="draft_ready",
                message="Discord webhook URL not configured.",
                payload=self.build_payload(request),
            )

        try:
            import httpx

            discord_payload = {
                "content": request.content,
                "username": request.metadata.get("bot_name", "Hyperskills Bot"),
                "embeds": [
                    {
                        "title": request.title or "New Post",
                        "description": request.content[:250],
                        "color": 6895456,
                    }
                ],
            }

            response = httpx.post(
                self.webhook_url,
                json=discord_payload,
                timeout=15,
            )

            if response.status_code == 204:
                return PlatformResult(
                    platform_id=self.platform_id,
                    status="published",
                    message="Message posted to Discord",
                    payload={
                        **self.build_payload(request),
                        "webhook_url": self.webhook_url,
                    },
                )
            else:
                return PlatformResult(
                    platform_id=self.platform_id,
                    status="failed",
                    message=f"Discord API error: {response.status_code}",
                    payload=self.build_payload(request),
                )
        except Exception as e:
            return PlatformResult(
                platform_id=self.platform_id,
                status="failed",
                message=f"Discord publish failed: {str(e)}",
                payload=self.build_payload(request),
            )


__all__ = ["RealLinkedInAdapter", "RealDiscordAdapter"]
