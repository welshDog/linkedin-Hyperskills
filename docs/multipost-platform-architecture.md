# MultiPost-inspired platform architecture

This repo now reflects the pattern from MultiPost, adapted to the founder-focused Hyperskills product.

## Core architecture pattern

The platform is built around a registry + adapter model:

- `PlatformAdapter` interface
- `PlatformRegistry` registry
- `PublishRequest` object
- `PlatformResult` tracking object
- `PublishOrchestrator` coordinating the publish flow

This keeps the content layer separate from the platform layer.

## What this means

Instead of one hardcoded publishing flow, we now have:

- one content object
- many platform targets
- platform-specific payload generation
- shared approval and safety checks

## Why this matters

It gives us the ability to publish to:

- LinkedIn
- Discord
- generic webhooks
- future channels like X, Substack, RSS, and newsletter tools

without rewriting the creator workflow.

## Current implementation

The repo includes:

- `src/platforms/common.py` with core platform contracts
- `src/platforms/linkedin.py` for LinkedIn adapter
- `src/platforms/discord.py` for Discord webhook posting
- `src/platforms/webhook.py` for generic payload delivery
- `src/publisher/orchestrator.py` for route orchestration

## Design principle

The product is structured so that:

- founder voice lives in the brand layer
- trust checks live in the approval layer
- publishing moves through the adapter layer
- analytics live in the tracking layer

This is the correct separation for product durability.

## Future extension

This architecture is ready for:

- X/Twitter publishing
- newsletter publishing
- RSS syndication
- campaign orchestration
- content scheduling
- performance-based route optimization

The build pattern is sound. The next step is real product wiring and founder testing.
