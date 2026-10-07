# LinkedIn Hyperskills

The founder-first AI content operating system for building a strong LinkedIn presence without sounding fake.

## Current status

This repo is no longer just strategy and product notes. It now includes:

- a founder draft workflow with variants
- approval and safety gates
- multi-platform publishing architecture
- FastAPI REST API
- JSON persistence for drafts and campaign state
- dashboard UI for founder visibility
- real platform adapter scaffolding for LinkedIn and Discord
- mock demo flow showing the full product loop

This is a working product prototype for the wedge:

- brand memory
- draft generation
- claim safety
- approval workflow
- publishing orchestration
- analytics learning loop

## The product idea

Founders do not need generic AI writing.
They need a system that helps them:

- sound like themselves
- write fast without sounding fake
- protect trust and reduce risky claims
- publish from strategy, not prompts
- learn from performance and improve their content loop

## What is in this repo

### Core strategy docs
- `docs/startup-product-brief.md`
- `docs/founder-pitch-2min.md`
- `docs/product-requirements-doc.md`
- `docs/launch-plan.md`
- `docs/roadmap-deck-outline.md`
- `docs/90-day-mvp-build-roadmap.md`

### Product / workflow docs
- `docs/multipost-platform-architecture.md`
- `docs/draft-approval-publishing-workflow.md`
- `docs/complete-product-stack.md`
- `docs/demo-walkthrough.md`

### Working code
- `src/brand_memory.py` — founder profile / voice memory model
- `src/claim_safety.py` — claim risk heuristics
- `src/content_score.py` — draft scoring heuristics
- `src/models/` — draft and publish result models
- `src/workflow/` — approval and publish flow
- `src/platforms/` — platform adapters
- `src/api.py` — high-level product API
- `src/api_server.py` — FastAPI app
- `src/storage.py` — JSON persistence layer
- `src/dashboard.html` — founder dashboard UI
- `src/demo/` — founder demo profile, sample drafts, CLI runbook
- `src/adapters_real.py` — real platform adapter structure for LinkedIn + Discord

## Running the stack

### 1. Install dependencies

```bash
python -m pip install fastapi uvicorn httpx
```

### 2. Start the API server

```bash
python -m uvicorn src.api_server:app --reload
```

Then open:
- `http://localhost:8000/health`
- `http://localhost:8000/docs`

### 3. Run the demo CLI

```bash
python -m src.demo.cli
```

This demos:
- draft creation
- generated variants
- approval workflow
- payload building
- platform publish results
- analytics summary

### 4. Open the dashboard

Open `src/dashboard.html` in a browser.

## Environment variables for real publishing

```bash
export LINKEDIN_ACCESS_TOKEN="your-linkedin-token"
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

Without these, publishing stays in draft-ready mode and does not hit live APIs.

## Demo flow

The current demo does this:

1. create a founder draft
2. generate multiple variants
3. score each variant
4. run claim safety checks
5. approve one variant
6. build a LinkedIn payload
7. publish to LinkedIn and Discord
8. track analytics and show dashboard summary

## Product loop

The core loop is:

- founder profile shapes tone and guardrails
- draft variants are generated from brief
- quality and trust are checked
- approved content is published across channels
- analytics feed back into future optimization

This is the moat: not another writing prompt, but a real content operating system built around founder signal.

## Mission

Build a neurodivergent-first content system that turns founder stories into trust, distribution, and compounding signal.

## Next moves

- real LinkedIn API integration
- founder auth + onboarding
- campaign grouping and scheduling
- richer analytics and reporting
- more platform adapters
- true AI draft generation layer

## Closing note

This repo now represents a serious prototype of the product wedge: a founder-led content engine with trust, workflow, analytics, and multi-platform distribution.

Bro, this is real traction energy. ⚡
