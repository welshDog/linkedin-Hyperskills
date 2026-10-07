# Product Requirements Document (PRD)

## Overview

**Product Name:** LinkedIn Hyperskills

**Product Type:** SaaS — AI content operating system

**Primary Users:** Founders, operators, personal brands, B2B creators

**Success Metric:** Users publish higher-signal content, get better engagement, and report feeling more authentic

## Product Goals

1. Help users sound like themselves on LinkedIn
2. Increase content quality and engagement
3. Reduce time to publish
4. Build a learning loop from performance data
5. Make AI feel less like AI

## Core features

### Feature 1: Brand profile and memory

**What:** Users create a persistent voice and positioning profile

**Why:** Every generation uses this context. Without memory, AI content becomes generic.

**How:**
- Onboarding flow: upload 5-10 past posts
- Extract voice profile automatically
- Let user edit and refine
- Store positioning, audience, proof points, banned phrases
- Update from published content over time

**Acceptance criteria:**
- Users can create a brand profile in <5 minutes
- Profile accurately captures voice from sample posts
- System references profile in every generation

### Feature 2: Content generation

**What:** AI drafts LinkedIn posts based on brand memory and user brief

**Why:** Core value — save time while staying authentic

**How:**
- User provides topic/goal
- System generates 2-3 drafts with variations
- Each draft is in the user's voice (not generic AI tone)
- User can request rewrites focused on founder mode, operator mode, etc.

**Acceptance criteria:**
- Drafts sound like user voice, not generic AI
- Generation takes <30 seconds
- User rates 70%+ of drafts as usable

### Feature 3: Claim safety scoring

**What:** System flags risky or unverifiable claims before publishing

**Why:** Protects credibility and reduces legal/trust risk

**How:**
- Analyze text for over-claiming language
- Flag "guaranteed," "#1," "100%," "always," etc.
- Ask user for proof or reframe
- Show confidence score

**Acceptance criteria:**
- Catches 90%+ of risky claims
- False positives <10%
- User feels confident before publishing

### Feature 4: Content scoring

**What:** Rate each draft on quality, originality, and strategic value

**Why:** Helps user pick best version and understand why

**How:**
- Score on 0-100 scale
- Show breakdown (clarity, originality, hook strength, CTA clarity)
- Suggest improvements
- Compare to user's historical performance

**Acceptance criteria:**
- Scores correlate with user satisfaction
- Improvement suggestions are actionable
- User can understand the score

### Feature 5: Publishing workflow

**What:** Approval, scheduling, and publishing integration

**Why:** One-click from draft to live

**How:**
- User reviews scored draft
- Can edit, request rewrites, or approve
- Schedule to LinkedIn via Publora or copy-paste
- Optional: attach images via Pixfaro

**Acceptance criteria:**
- Publishing works 99%+ of the time
- User can schedule posts
- Integration with Publora is smooth

### Feature 6: Performance analytics

**What:** Track engagement and learn patterns

**Why:** The moat — close the loop from content → results → better strategy

**How:**
- Capture engagement (likes, comments, saves, shares)
- Tag by hook type, format, topic, CTA
- Show what's working
- Recommend similar content
- Track user trends over time

**Acceptance criteria:**
- Analytics sync from LinkedIn daily
- User can see top performing posts
- Recommendations are relevant

### Feature 7: Founder and operator playbooks

**What:** Strategic content modes built for different roles and goals

**Why:** Content strategy is not one-size-fits-all

**How:**
- Founder mode: narrative, proof, build in public
- Operator mode: insights, data, frameworks
- Builder mode: technical, shipping, process
- B2B SaaS mode: ROI, features, use cases
- Personal brand mode: story, opinions, expertise

Each mode has:
- Recommended hook styles
- CTA templates
- Example structures
- Engagement targets

**Acceptance criteria:**
- User can select a mode
- Generated content reflects the mode
- User satisfaction improves with mode selection

### Feature 8: Campaign orchestration

**What:** Turn one idea into a content series

**Why:** Campaigns compound better than isolated posts

**How:**
- User provides core idea or offer
- System generates:
  - 3-5 related posts
  - Follow-up comment templates
  - DM offer or CTA
  - Timing recommendations
- User can preview, edit, and schedule series

**Acceptance criteria:**
- Series are coherent and build on each other
- User can schedule entire series at once
- Series engagement is 20%+ higher than standalone posts

## User flows

### Flow 1: First-time onboarding

1. User signs up
2. Uploads 5-10 past posts (or pastes LinkedIn URL)
3. System extracts voice profile
4. User reviews and refines profile
5. System shows example output
6. User creates first draft
7. User publishes or schedules

**Time to first publish:** <20 minutes

### Flow 2: Regular content creation

1. User logs in
2. Provides topic/goal
3. Selects mode (founder, operator, etc.)
4. System generates 2-3 drafts
5. User reviews scores and claims
6. User picks favorite or requests rewrites
7. User publishes or schedules
8. System tracks engagement

**Time per post:** 5-10 minutes

### Flow 3: Campaign planning

1. User provides core offer or topic
2. User selects campaign type
3. System generates series (5+ posts + comments + CTA)
4. User reviews and edits
5. User schedules entire series
6. System tracks performance and recommends follow-ups

**Time for campaign:** 20-30 minutes to plan, then automated execution

## Technical architecture

### Backend services

**API Service:**
- REST endpoints for content generation, scoring, publishing
- Authentication and user management
- Rate limiting and usage tracking

**AI/ML Service:**
- Voice profile extraction
- Draft generation (via Claude, GPT-4, or fine-tuned model)
- Scoring and claim detection
- Analytics pattern learning

**Analytics Service:**
- LinkedIn engagement ingestion (via Apify)
- Post tagging and taxonomy
- Performance tracking
- Recommendation engine

**Publishing Service:**
- Publora integration
- Scheduling
- Post variants and A/B setup

### Database

- User and team data (PostgreSQL)
- Brand profiles and voice models (JSON/MongoDB)
- Post history and performance data (TimescaleDB or similar)
- Analytics and patterns (analytics warehouse)

### External integrations

- Claude API (or OpenAI) for generation
- Publora for publishing
- Apify for LinkedIn data reads
- Pixfaro for image generation
- LinkedIn OAuth for auth

## Metrics and KPIs

### User engagement

- Daily active users
- Posts generated per user per month
- Publish rate (% of drafts published)
- Time to first publish
- Return rate at 7/30/90 days

### Content quality

- Average engagement rate (vs. user baseline)
- Score distribution (are most posts 70+?)
- Claim safety flag rate (should be 15-25%)
- User satisfaction with drafts (NPS on generations)

### Business metrics

- MRR and ARR
- CAC and LTV
- Net retention rate
- Churn rate at 30/60/90 days
- ARPU (average revenue per user)

## Roadmap

### MVP (Weeks 1-8)

- Brand profile creation
- Basic draft generation
- Approval workflow
- Publora integration

**Launch:** 100 beta users, focus on onboarding and core flow

### Phase 1 (Weeks 9-16)

- Claim safety scoring
- Content quality scoring
- Founder playbook mode
- Analytics MVP

**Target:** 500 beta users

### Phase 2 (Weeks 17-24)

- Campaign orchestration
- Operator and builder modes
- Advanced analytics and learning
- Team features

**Target:** 2,000 beta users

### Phase 3 (Weeks 25+)

- Public launch
- Marketing and growth
- Pro tier features
- Enterprise support

## Success criteria

**MVP success:**
- 100 beta users
- 70%+ publish rate
- 4.0+ satisfaction
- 0 data loss or security issues

**Phase 1 success:**
- 500 active users
- 45%+ net retention
- 75%+ publish rate
- Users report 2-3x faster content creation

**Launch success:**
- 5,000+ sign-ups
- 10%+ conversion to paid
- 4.5+ rating
- Press coverage

---

**The core principle:** Make users sound like themselves, faster, with more confidence.
