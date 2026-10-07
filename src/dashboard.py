from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.analytics import AnalyticsEngine
from src.models import Draft


class FounderDashboard:
    """Simple dashboard view for founder content performance and pipeline status."""

    def __init__(self, analytics_engine: Optional[AnalyticsEngine] = None):
        self.analytics = analytics_engine or AnalyticsEngine()

    def build_summary(self, drafts: List[Draft]) -> Dict[str, Any]:
        """Build a founder-friendly summary for multiple drafts."""
        draft_summaries = []
        total_published = 0
        total_failed = 0
        total_variants = 0

        for draft in drafts:
            analytics = self.analytics.summarize_draft(draft.draft_id)
            draft_summaries.append(
                {
                    "draft_id": draft.draft_id,
                    "title": draft.title,
                    "status": draft.status.value,
                    "platforms": draft.platforms,
                    "approved_variants": sum(1 for v in draft.variants if v.approved),
                    "analytics": analytics,
                }
            )
            total_variants += len(draft.variants)

        return {
            "total_drafts": len(drafts),
            "total_variants": total_variants,
            "drafts": draft_summaries,
            "best_platform": self._best_platform(drafts),
        }

    def _best_platform(self, drafts: List[Draft]) -> Optional[str]:
        all_platforms = []
        for draft in drafts:
            all_platforms.extend(draft.platforms)
        if not all_platforms:
            return None
        counts = {}
        for platform in all_platforms:
            counts[platform] = counts.get(platform, 0) + 1
        return max(counts.items(), key=lambda item: item[1], default=(None, 0))[0]

    def render_cli(self, drafts: List[Draft]) -> str:
        summary = self.build_summary(drafts)
        lines = [
            "Founder Dashboard",
            "=================",
            f"Total drafts: {summary['total_drafts']}",
            f"Total variants: {summary['total_variants']}",
            f"Best platform: {summary['best_platform'] or 'n/a'}",
            "",
        ]
        for item in summary["drafts"]:
            lines.append(f"- {item['title']} [{item['status']}]")
            lines.append(f"  Approved variants: {item['approved_variants']}")
            lines.append(f"  Engagement rate: {item['analytics']['avg_engagement_rate']}%")
        return "\n".join(lines)


__all__ = ["FounderDashboard"]
