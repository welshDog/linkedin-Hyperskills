# Draft → Approval → Publishing Workflow

This document describes the complete workflow for turning a founder's brief into an approved, multi-platform post.

## Architecture Layers

```
┌─────────────────────────────────────┐
│   Founder Input                     │
│   (brief, title, platforms)         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Draft Model                       │
│   (variants, status machine)        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Approval Engine                   │
│   (score → claims → approve)        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Publish Workflow                  │
│   (route to platforms)              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Result Tracker                    │
│   (published/failed per platform)   │
└─────────────────────────────────────┘
```

## Data Models

### Draft
A founder's post draft with multiple variants.

```python
@dataclass
class Draft:
    founder_id: str
    title: str
    brief: str
    variants: List[Variant]
    status: DraftStatus
    platforms: List[str]
    scheduled_for: Optional[str]
```

### Variant
A single draft variant candidate.

```python
@dataclass
class Variant:
    content: str
    score: Optional[float]
    claim_risk: Optional[str]  # low/medium/high
    approved: bool
```

### PublishResult
Tracking record for each published post.

```python
@dataclass
class PublishResult:
    draft_id: str
    variant_id: str
    platform_id: str
    status: PublishResultStatus  # published/failed/scheduled
    url: Optional[str]
    error_message: Optional[str]
```

## Workflow Steps

### 1. Create Draft

```python
draft = Draft(
    founder_id="founder-123",
    title="Why I left the rat race",
    brief="Personal story about leaving corporate",
    platforms=["linkedin", "discord"],
)
```

### 2. Generate Variants

Add multiple draft variants.

```python
variant_1 = draft.add_variant("I quit my job after...")
variant_2 = draft.add_variant("Here's why I left corporate...")
variant_3 = draft.add_variant("The truth about leaving my job...")
```

### 3. Run Approval Workflow

Score, check claims, approve.

```python
approval_engine = ApprovalEngine()

# Run full approval on variant 1
approved = approval_engine.approve_workflow(draft, variant_1.variant_id)

if approved:
    print("✅ Variant approved for publishing")
else:
    print("⚠️ Variant flagged or rejected")
```

### 4. Publish to Platforms

Once approved, publish to all configured platforms.

```python
workflow = PublishWorkflow(orchestrator, tracker)

results = workflow.publish_approved_draft(
    draft,
    variant_1.variant_id,
)

for result in results:
    print(f"{result.platform_id}: {result.status}")
```

### 5. Track Results

Monitor publishing success across platforms.

```python
status = workflow.get_draft_status(draft)
print(f"Published: {status['published']}")
print(f"Failed: {status['failed']}")
print(f"Success rate: {status['success_rate']:.1f}%")
```

## Status Transitions

```
CREATED
  │
  ├─→ SCORING
  │    │
  │    └─→ SAFETY_CHECK
  │         │
  │         ├─→ FLAGGED (high-risk claims)
  │         │
  │         └─→ SCORED
  │              │
  │              └─→ APPROVED
  │                   │
  │                   └─→ PUBLISHING
  │                        │
  │                        ├─→ PUBLISHED ✅
  │                        │
  │                        └─→ FAILED ❌
  │
  └─→ REJECTED
```

## Platform Adapters

Each platform (LinkedIn, Discord, Webhook) has a payload builder and publisher.

### LinkedIn

```python
builder = LinkedInPostPayloadBuilder(variant, founder_profile)
payload = builder.build()
# Returns: { text, visibility, content, distribution }
```

### Discord

Uses webhook to post directly to channels.

### Webhook

Generic webhook adapter for custom endpoints.

## Next Steps

1. **Brand Memory Integration**: Use founder's brand profile to score and filter variants.
2. **Analytics Loop**: Track engagement and learn from published posts.
3. **Scheduling**: Support scheduled publishing across time zones.
4. **Draft Revision**: Allow rejecting and regenerating variants.
5. **Campaign Tracking**: Group related drafts into campaigns.
