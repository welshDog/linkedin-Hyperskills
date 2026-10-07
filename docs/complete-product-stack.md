# Complete Product Stack

This repo now represents a working founder content operating system, not just a concept deck.

## Current architecture

```text
Founder profile + brief
        ↓
Draft model + variants
        ↓
Approval engine
        ↓
Publish workflow
        ↓
Platform adapters
        ↓
Analytics + dashboard
```

## Product layers

### 1. Brand layer
- founder profile
- tone and banned phrases
- proof points and positioning
- trust guardrails
- claim-risk filters

### 2. Draft workflow layer
- draft creation
- multiple variants
- scoring
- approval state machine
- revision pipeline

### 3. Publishing layer
- LinkedIn adapter
- Discord adapter
- generic webhook adapter
- platform registry
- publish orchestrator

### 4. Analytics layer
- result tracking
- engagement metrics
- per-draft summary
- best platform identification
- performance loop

### 5. Product layer
- FastAPI backend
- JSON storage
- dashboard UI
- campaign view
- founder-facing summaries

## Current repository structure

```text
src/
├── api.py
├── api_server.py
├── analytics.py
├── dashboard.html
├── dashboard.py
├── multipost_architecture.py
├── storage.py
├── adapters_real.py
├── models/
│   ├── draft.py
│   ├── publish_result.py
│   └── __init__.py
├── workflow/
│   ├── approval_engine.py
│   ├── publish_workflow.py
│   └── __init__.py
├── platforms/
│   ├── common.py
│   ├── linkedin.py
│   ├── discord.py
│   ├── webhook.py
│   └── __init__.py
├── payloads/
│   ├── linkedin_payload.py
│   └── __init__.py
├── tracking/
│   ├── result_tracker.py
│   └── __init__.py
├── demo/
│   ├── sample_founder.py
│   ├── sample_drafts.py
│   ├── cli.py
│   ├── mock_results.py
│   └── __init__.py
├── brand_memory.py
├── claim_safety.py
├── content_score.py
└── __init__.py
```

## What works right now

- founder draft creation through the API
- variant generation and approval state transitions
- platform adapter registry
- LinkedIn and Discord payload shaping
- mock results and analytics tracking
- dashboard rendering
- JSON persistence for drafts

## How to run it

### Start the API

```bash
python -m uvicorn src.api_server:app --reload
```

### Run the demo CLI

```bash
python -m src.demo.cli
```

### Open the dashboard

Open `src/dashboard.html` directly or serve it through a local static server.

## Real platform readiness

### LinkedIn
- real API structure exists
- requires `LINKEDIN_ACCESS_TOKEN`
- response handling is built for `ugcPosts`-style integration

### Discord
- real webhook adapter exists
- requires `DISCORD_WEBHOOK_URL`
- posts via webhook embed payload

## Persistence model

Drafts are stored under `data/drafts/` in JSON format for easy iteration.

This gives us a clear path to a database later without rewriting the product logic.

## Product loop

1. create founder brief
2. generate variants
3. score and safety-check content
4. approve variant
5. publish to LinkedIn / Discord / webhook
6. track performance
7. improve future content from evidence

## This is the product wedge

The real wedge is not generic AI writing.
The wedge is:

- founder-specific memory
- trust-safe publishing
- content systematization
- analytics-driven optimization
- multi-platform execution

That is a serious platform foundation.

## Next technical milestone

The next step is to move from prototype to founder live testing:

- founder onboarding
- real auth
- database persistence
- real platform API connectors
- richer reporting
- campaign scheduling
- performance feedback loops
