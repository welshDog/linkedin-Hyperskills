# Technical data model

## Product data model

At MVP, the system needs a small but strong backbone.

### Core objects

1. User
2. Brand profile
3. Draft
4. Post
5. Publishing job
6. Engagement metric

## PostgreSQL core schema

### users
- id
- email
- username
- password_hash
- linkedin_id
- created_at
- updated_at
- subscription_tier

### orgs
- id
- name
- owner_id
- created_at

### posts
- id
- user_id
- content
- status
- created_at
- updated_at
- scheduled_at
- published_at
- published_url
- score_overall
- claim_risk

### post_metrics
- id
- post_id
- likes
- comments
- shares
- saves
- impressions
- engagement_rate
- captured_at

## MongoDB flexible documents

### brand_profiles
```json
{
  "user_id": "uuid",
  "positioning": "founder-led SaaS operator",
  "audience": "B2B founders and operators",
  "tone": "clear, candid, practical",
  "values": ["clarity", "proof", "execution"],
  "proof_points": ["real numbers", "real decisions", "real lessons"],
  "banned_phrases": ["leverage", "unlock", "synergy"],
  "strong_hooks": ["why this mattered", "what changed", "what I learned"],
  "weak_signals": ["generic motivation", "hype language"]
}
```

### drafts
```json
{
  "draft_id": "uuid",
  "user_id": "uuid",
  "topic": "how to package founder story for LinkedIn",
  "content": "...",
  "scores": {
    "overall": 82,
    "clarity": 88,
    "hook": 80,
    "trust": 76
  },
  "claim_flags": ["overconfident promise"],
  "status": "draft"
}
```

## Redis usage

- session cache
- app rate limiting
- draft generation queue
- recent profile cache

## S3 usage

- uploaded sample posts
- export files
- any visual assets or slide exports

## Critical relationships

- user → brand profile
- user → posts
- post → engagement metrics
- post → draft history

## Data principles

- user content remains user-owned
- trust checks are stored with content
- scores and safety flags are explicit and visible
- analytics are additive, not hidden

This is a simple but strong base that supports the MVP and future evolution.
