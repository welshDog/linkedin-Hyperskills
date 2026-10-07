# Multi-post publish architecture
# This is the product skeleton for a MultiPost-inspired platform strategy.
# It keeps the founder brand layer, adds a channel adapter layer, and makes publishing modular.

from __future__ import annotations

from src.platforms import DiscordAdapter, LinkedInAdapter, PlatformRegistry, WebhookAdapter
from src.publisher import PublishOrchestrator


def build_default_registry() -> PlatformRegistry:
    registry = PlatformRegistry()
    registry.register(LinkedInAdapter())
    registry.register(DiscordAdapter())
    registry.register(WebhookAdapter())
    return registry


def build_default_orchestrator() -> PublishOrchestrator:
    return PublishOrchestrator(registry=build_default_registry())


__all__ = ["build_default_registry", "build_default_orchestrator"]
