from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

from src.models import PublishResult, PublishResultStatus


class PublishResultTracker:
    """Tracks all publishing results for drafts across platforms."""

    def __init__(self) -> None:
        self._results: List[PublishResult] = []
        self._by_draft: Dict[str, List[PublishResult]] = defaultdict(list)
        self._by_platform: Dict[str, List[PublishResult]] = defaultdict(list)

    def record(self, result: PublishResult) -> None:
        """Record a new publish result."""
        self._results.append(result)
        self._by_draft[result.draft_id].append(result)
        self._by_platform[result.platform_id].append(result)

    def get_draft_results(self, draft_id: str) -> List[PublishResult]:
        """Get all publishing results for a draft."""
        return self._by_draft.get(draft_id, [])

    def get_platform_results(self, platform_id: str) -> List[PublishResult]:
        """Get all results for a specific platform."""
        return self._by_platform.get(platform_id, [])

    def get_published_count(self, draft_id: str) -> int:
        """Count successfully published posts for a draft."""
        return sum(
            1
            for r in self._by_draft.get(draft_id, [])
            if r.status == PublishResultStatus.PUBLISHED
        )

    def get_failed_count(self, draft_id: str) -> int:
        """Count failed posts for a draft."""
        return sum(
            1
            for r in self._by_draft.get(draft_id, [])
            if r.status == PublishResultStatus.FAILED
        )

    def get_success_rate(self, draft_id: str) -> float:
        """Calculate success rate for a draft across all platforms."""
        results = self._by_draft.get(draft_id, [])
        if not results:
            return 0.0
        published = self.get_published_count(draft_id)
        return (published / len(results)) * 100.0

    def get_all_results(self) -> List[PublishResult]:
        """Get all tracking results."""
        return self._results.copy()

    def summary(self, draft_id: str) -> Dict[str, int]:
        """Get a summary of publishing results for a draft."""
        results = self._by_draft.get(draft_id, [])
        status_counts = defaultdict(int)
        for result in results:
            status_counts[result.status.value] += 1
        return dict(status_counts)


__all__ = ["PublishResultTracker"]
