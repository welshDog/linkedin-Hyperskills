# App architecture overview

## High-level architecture

LinkedIn Hyperskills is a modular SaaS product made of a small number of message-heavy services:

- auth and user service
- brand memory service
- content generation service
- safety and scoring service
- publishing service
- analytics service

The product is designed to be simple to build and strong enough to scale.

## Core architecture pattern

The system follows a simple loop:

1. learn the user’s brand profile
2. generate a draft from a brief
3. score the draft and check for claim risk
4. let the user approve or reject
5. publish or schedule the final content
6. capture outcomes and improve future drafts

That loop is the product.

## Services

### Auth service
Responsibilities:
- signup/login
- session management
- user profiles
- LinkedIn auth integration

### Brand memory service
Responsibilities:
- store voice and audience profile
- extract voice from uploaded sample posts
- keep proof points and tone signals
- persist brand state for future generation

### Content generation service
Responsibilities:
- accept brief and brand profile
- produce 2-3 variants in the user’s voice
- support founder/operator modes later

### Safety and scoring service
Responsibilities:
- quality scoring
- claim-risk detection
- hook and CTA assessment
- improvement suggestions

### Publishing service
Responsibilities:
- approval workflow
- publish/schedule actions
- API integration with publishing service
- fallback copy-paste if needed

### Analytics service
Responsibilities:
- track performance after publishing
- store engagement and content outcomes
- enable learning and recommendations later

## Data layer

Primary stores:
- PostgreSQL for users, posts, orgs, subscriptions
- MongoDB for flexible brand profiles and content metadata
- Redis for cache and queues
- TimescaleDB or equivalent for analytics
- S3 for assets and exports

## External integrations

- Claude or OpenAI for generation
- LinkedIn OAuth for auth and account access
- Publora for publishing
- Apify for read-side engagement and performance data
- Pixfaro for image generation later
- Stripe for billing downstream

## Security model

- JWT-based auth
- OAuth for LinkedIn access
- RBAC for team and org access
- secret management for API keys
- encrypted storage for sensitive data
- API rate limiting and request logging

## Why this architecture fits the product

This system is intentionally simple and modular. It supports:

- fast MVP delivery
- fewer failure points
- easier iteration
- clearer rollout and testing
- future platform expansion without rewiring the whole stack

## Key principle

Do not build complexity before the wedge is proven.
The first app should do the four things users need most:

- remember the user
- generate drafts
- flag risk
- approve before publishing
