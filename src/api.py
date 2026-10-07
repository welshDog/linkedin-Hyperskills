from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.analytics import AnalyticsEngine
from src.multipost_architecture import build_default_orchestrator
from src.models import Draft, DraftStatus, PublishResult, Variant
from src.workflow import ApprovalEngine, PublishWorkflow


class HyperskillsAPI:
    """High-level founder operations API for the LinkedIn Hyperskills platform."""

    def __init__(self, orchestrator=None, analytics_engine: Optional[AnalyticsEngine] = None):
        self.orchestrator = orchestrator or build_default_orchestrator()
        self.workflow = PublishWorkflow(
            orchestrator=self.orchestrator,
            tracker=self.orchestrator.tracker if hasattr(self.orchestrator, "tracker") else None,
        )
        self.analytics = analytics_engine or AnalyticsEngine()

    def create_draft(
        self,
        founder_id: str,
        title: str,
        brief: str,
        platforms: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        scheduled_for: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Draft:
        draft = Draft(
            founder_id=founder_id,
            title=title,
            brief=brief,
            platforms=platforms or ["linkedin"],
            tags=tags or [],
            scheduled_for=scheduled_for,
            metadata=metadata or {},
        )
        return draft

    def add_variant(self, draft: Draft, content: str) -> Variant:
        return draft.add_variant(content)

    def approve_variant(self, draft: Draft, variant_id: str) -> bool:
        engine = ApprovalEngine()
        return engine.approve_workflow(draft, variant_id)

    def publish_approved_variant(self, draft: Draft, variant_id: str):
        if self.workflow is None:
            raise RuntimeError("No publish workflow is configured.")
        results = self.workflow.publish_approved_draft(draft, variant_id)
        for result in results:
            self.analytics.track_result(result)
        return results

    def get_draft_summary(self, draft: Draft) -> Dict[str, Any]:
        return {
            "draft": draft.to_dict(),
            "approval_summary": ApprovalEngine().get_approval_summary(draft),
            "publish_status": self.workflow.get_draft_status(draft) if self.workflow else {},
            "analytics": self.analytics.summarize_draft(draft.draft_id),
        }


__all__ = ["HyperskillsAPI"]
