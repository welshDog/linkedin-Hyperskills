from __future__ import annotations

from typing import Iterable, List, Optional, Sequence

from .common import PlatformAdapter, PlatformRegistry, PlatformResult, PublishRequest


class PublishOrchestrator:
    """Runs a founder draft through trust checks and multiple platform adapters."""

    def __init__(self, registry: Optional[PlatformRegistry] = None) -> None:
        self.registry = registry or PlatformRegistry()

    def register(self, adapter: PlatformAdapter) -> None:
        self.registry.register(adapter)

    def targets(self, platform_ids: Optional[Sequence[str]]) -> List[str]:
        if not platform_ids:
            return list(self.registry.list_platforms())
        return list(platform_ids)

    def publish(self, request: PublishRequest) -> List[PlatformResult]:
        results: List[PlatformResult] = []
        for platform_id in self.targets(request.platform_ids):
            adapter = self.registry.get(platform_id)
            if adapter is None:
                results.append(
                    PlatformResult(
                        platform_id=platform_id,
                        status="unsupported",
                        message="Platform adapter is not registered yet.",
                        payload={"requested": platform_id},
                    )
                )
                continue
            results.append(adapter.publish(request))
        return results


__all__ = ["PublishOrchestrator"]
