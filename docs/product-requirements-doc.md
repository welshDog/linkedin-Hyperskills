# Product requirements document

## Overview

Product name: LinkedIn Hyperskills

Product type: AI content operating system for founder-led LinkedIn growth

Primary users:
- founders
- operators
- personal brands
- B2B creators

## Product goal

Help users publish high-signal LinkedIn content in their own voice without spending hours writing or risking credibility.

## Core user problem

Users need:
- faster content creation
- authentic voice
- risk-aware publishing
- strategic content planning
- less wasted time

## MVP scope

The MVP focuses on the wedge:

- brand memory
- draft generation
- claim safety
- approval workflow

No broad feature expansion before this is proven.

## User stories

### 1. Brand memory
- As a user, I want my profile and voice stored so generated content feels like me.
- As a user, I want to upload sample posts and tune my profile.
- As a user, I want guidance on my audience, tone, and proof points.

### 2. Draft generation
- As a user, I want to generate 2-3 LinkedIn post variants from a topic.
- As a user, I want the draft in my tone, not generic AI tone.
- As a user, I want to choose a mode like founder or operator.

### 3. Claim safety
- As a user, I want to know before publishing if my draft makes risky claims.
- As a user, I want suggestions to tighten or reframe weak claims.

### 4. Approval workflow
- As a user, I want to review the draft before it goes live.
- As a user, I want to edit, approve, or reject it.
- As a user, I want a publishing option or scheduling option.

## Functional requirements

### Brand profile
- user can create profile
- user can add voice and audience information
- user can upload sample text
- system stores and recalls profile data

### Draft generation
- user enters brief or topic
- system generates 2-3 variants
- system uses stored brand memory
- each draft includes a hook and CTA

### Quality and safety scoring
- score clarity, originality, hook, CTA, and trust level
- flag risky claim language
- show improvement suggestions

### Approval flow
- user can approve or reject draft
- user can edit before publishing
- saved draft is tracked as one record in the user content history

### Publishing
- provide publish or schedule action
- store published URL and status
- offer fallback copy-paste if publish fails

## Non-functional requirements

- generation < 30s for MVP
- score generation < 5s
- clear API error states
- JWT auth and role controls
- privacy-safe storage of user data
- minimal but production-ready logging

## Success metrics

- draft completion time
- post approval rate
- publish success rate
- active users in beta
- user satisfaction with authenticity and speed

## Out of scope for MVP

- campaign orchestration
- team workflows
- analytics loops beyond basic publish metrics
- advanced image generation
- white-label features
- enterprise features

## Done criteria

The MVP is successful when a user can:

- set up a brand profile
- generate content in their voice
- inspect score and safety warnings
- approve before publishing
- publish or schedule a post

That is the wedge.
