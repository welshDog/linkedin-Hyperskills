from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PerformanceSignal:
    """A single platform performance event for one draft variant."""

    draft_id: str
    variant_id: str
    platform_id: str
    impressions: int = 0
    engagements: int = 0
    clicks: int = 0
    reactions: int = 0
    comments: int = 0
    shares: int = 0
    published_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def engagement_rate(self) -> float:
        if self.impressions <= 0:
            return 0.0
        return (self.engagements / self.impressions) * 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "draft_id": self.draft_id,
            "variant_id": self.variant_id,
            "platform_id": self.platform_id,
            "impressions": self.impressions,
            "engagements": self.engagements,
            "clicks": self.clicks,
            "reactions": self.reactions,
            "comments": self.comments,
            "shares": self.shares,
            "published_at": self.published_at,
            "engagement_rate": self.engagement_rate,
            "metadata": self.metadata,
        }


class AnalyticsEngine:
    """Collects and summarizes founder content performance across platforms."""

    def __init__(self) -> None:
        self._signals: List[PerformanceSignal] = []
        self._by_draft: Dict[str, List[PerformanceSignal]] = {}

    def track_result(self, result: Any, metrics: Optional[Dict[str, Any]] = None) -> None:
        """Track a published result and optional performance metrics."""
        metrics = metrics or {}
        signal = PerformanceSignal(
            draft_id=getattr(result, "draft_id", "unknown"),
            variant_id=getattr(result, "variant_id", "unknown"),
            platform_id=getattr(result, "platform_id", "unknown"),
            impressions=int(metrics.get("impressions", 0)),
            engagements=int(metrics.get("engagements", 0)),
            clicks=int(metrics.get("clicks", 0)),
            reactions=int(metrics.get("reactions", 0)),
            comments=int(metrics.get("comments", 0)),
            shares=int(metrics.get("shares", 0)),
            published_at=getattr(result, "published_at", None),
            metadata={"status": getattr(result, "status", "unknown").value if hasattr(result, "status") else "unknown"},
        )
        self._signals.append(signal)
        self._by_draft.setdefault(signal.draft_id, []).append(signal)

    def summarize_draft(self, draft_id: str) -> Dict[str, Any]:
        signals = self._by_draft.get(draft_id, [])
        if not signals:
            return {
                "draft_id": draft_id,
                "total_posts": 0,
                "total_impressions": 0,
                "total_engagements": 0,
                "avg_engagement_rate": 0.0,
                "best_platform": None,
            }

        total_impressions = sum(s.impressions for s in signals)
        total_engagements = sum(s.engagements for s in signals)
        avg_rate = (total_engagements / total_impressions * 100.0) if total_impressions else 0.0

        platform_scores = {}
        for signal in signals:
            platform_scores[signal.platform_id] = platform_scores.get(signal.platform_id, 0) + signal.engagements
        best_platform = max(platform_scores.items(), key=lambda item: item[1], default=(None, 0))[0]

        return {
            "draft_id": draft_id,
            "total_posts": len(signals),
            "total_impressions": total_impressions,
            "total_engagements": total_engagements,
            "avg_engagement_rate": round(avg_rate, 2),
            "best_platform": best_platform,
        }

    def get_all_signals(self) -> List[PerformanceSignal]:
        return list(self._signals)


__all__ = ["AnalyticsEngine", "PerformanceSignal"]
