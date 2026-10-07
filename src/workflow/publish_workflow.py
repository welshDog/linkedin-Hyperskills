from __future__ import annotations

from typing import List

from src.models import Draft, DraftStatus, PublishResult, PublishResultStatus
from src.platforms import PublishRequest
from src.publisher import PublishOrchestrator
from src.tracking import PublishResultTracker


class PublishWorkflow:
    """Orchestrates the end-to-end publish workflow: approve → publish → track."""

    def __init__(
        self,
        orchestrator: PublishOrchestrator,
        tracker: PublishResultTracker,
    ) -> None:
        self.orchestrator = orchestrator
        self.tracker = tracker

    def publish_approved_draft(
        self,
        draft: Draft,
        variant_id: str,
    ) -> List[PublishResult]:
        """
        Publish an approved draft variant to all configured platforms.
        """
        # Verify the variant is approved
        variant = None
        for v in draft.variants:
            if v.variant_id == variant_id and v.approved:
                variant = v
                break

        if not variant:
            return []

        draft.set_status(DraftStatus.PUBLISHING)

        # Build publish request
        publish_request = PublishRequest(
            content=variant.content,
            title=draft.title,
            tags=draft.tags,
            platform_ids=draft.platforms,
            scheduled_for=draft.scheduled_for,
            metadata={
                "draft_id": draft.draft_id,
                "variant_id": variant.variant_id,
                "variant_score": variant.score,
                "claim_risk": variant.claim_risk,
                **draft.metadata,
            },
        )

        # Publish to all platforms via orchestrator
        platform_results = self.orchestrator.publish(publish_request)

        # Track all results
        tracked_results = []
        for platform_result in platform_results:
            result = PublishResult(
                draft_id=draft.draft_id,
                variant_id=variant.variant_id,
                platform_id=platform_result.platform_id,
            )

            if platform_result.status == "published":
                result.mark_published(
                    external_id=platform_result.payload.get("post_id", ""),
                    url=platform_result.payload.get("post_url"),
                )
            elif platform_result.status == "scheduled":
                result.mark_scheduled()
            else:
                result.mark_failed(platform_result.message)

            self.tracker.record(result)
            tracked_results.append(result)

        # Update draft status
        if self.tracker.get_failed_count(draft.draft_id) == 0:
            draft.set_status(DraftStatus.PUBLISHED)
        else:
            draft.set_status(DraftStatus.FAILED)

        return tracked_results

    def get_draft_status(self, draft: Draft) -> dict:
        """Get full status of a draft and its publishing results."""
        results = self.tracker.get_draft_results(draft.draft_id)
        return {
            "draft_id": draft.draft_id,
            "status": draft.status.value,
            "published": self.tracker.get_published_count(draft.draft_id),
            "failed": self.tracker.get_failed_count(draft.draft_id),
            "success_rate": self.tracker.get_success_rate(draft.draft_id),
            "platform_results": [r.to_dict() for r in results],
        }


__all__ = ["PublishWorkflow"]
