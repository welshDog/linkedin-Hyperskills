# Architecture

## Overview

The system should behave like a content operating system, not a one-shot text generator.

The core loop is:

1. Learn the user’s voice and intent
2. Generate a draft
3. Score the draft for quality and risk
4. Ask for approval
5. Publish or schedule
6. Capture results
7. Improve the next round

## Core components

### 1. Brand memory

A persistent model that captures:

- voice profile
- founder story
- strategic goals
- audience
- proof points
- banned language
- signal patterns

This is the memory layer. Without it, AI content becomes generic fast.

### 2. Draft generation layer

Generates content based on:

- brand memory
- topic brief
- audience fit
- hook requirements
- CTA goals

### 3. Risk and claim safety layer

Before publishing, it checks:

- over-claiming
- unsupported ROI language
- credibility gaps
- weak or empty proof
- AI tell density
- audience mismatch

### 4. Scoring and prioritization

A scoring engine rates content by:

- originality
- clarity
- strategic value
- trustworthiness
- signal strength
- audience fit

### 5. Analytics loop

This is the missing moat.

The system should store:

- hook type
- format
- CTA style
- topic category
- engagement data
- comment quality
- save/share rate

Then recommend future content based on what worked.

### 6. Campaign orchestration

A content system should not stop at one post. It should generate:

- related posts
- follow-up comments
- sequence variants
- offers and CTAs
- engagement prompts

## Technology shape

A good implementation could include:

- Python services for scoring and safety
- structured JSON memory files or a lightweight database
- markdown or YAML content briefs
- analytics ingestion layer
- optional integration with Publora, Apify, and Pixfaro

## Core principle

The product should optimize for trust, repeatability, and strategic signal.

Not raw volume.

## Resource model

The repo is best treated as a blueprint for an internal, modular system with these layers:

- memory
- generation
- scoring
- publishing
- analytics
- feedback

This makes it easier to grow from prototype to real product.
