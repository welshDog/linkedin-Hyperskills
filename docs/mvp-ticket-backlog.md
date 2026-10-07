# MVP task backlog

## Epic 1: User onboarding and brand memory

### Story 1: User sign up and login
**Priority:** P0  
**Owner:** Backend + Frontend  
**Acceptance criteria:**
- user can create account
- user can log in
- JWT auth works
- account is isolated by user

### Story 2: Create initial brand profile
**Priority:** P0  
**Acceptance criteria:**
- user enters audience, tone, value proposition
- profile saves to database
- profile loads on dashboard

### Story 3: Upload sample posts and extract voice profile
**Priority:** P0  
**Acceptance criteria:**
- user uploads 5-10 posts
- voice is extracted
- user can edit values before saving
- profile updates in database

### Story 4: Save and retrieve brand memory
**Priority:** P0  
**Acceptance criteria:**
- profile is re-used in generation requests
- cached profile loads quickly
- empty / invalid profile handled properly

---

## Epic 2: Draft generation

### Story 5: Generate 2-3 LinkedIn post variants
**Priority:** P0  
**Acceptance criteria:**
- input contains topic + context
- generation returns 2-3 drafts
- each draft has a hook and CTA
- drafts are stored to database

### Story 6: Support content modes
**Priority:** P1  
**Acceptance criteria:**
- founder mode uses founder framing
- operator mode uses operational voice
- basic mode gives default style

### Story 7: Save generation metadata
**Priority:** P1  
**Acceptance criteria:**
- saves model, prompt, timestamp, topic
- can be displayed in dashboard later

---

## Epic 3: Claim safety and scoring

### Story 8: Score draft quality
**Priority:** P0  
**Acceptance criteria:**
- draft receives clarity / originality / trust score
- user sees score breakdown
- low-score posts flagged clearly

### Story 9: Warn on risky claims
**Priority:** P0  
**Acceptance criteria:**
- claim safety checker catches obvious over-claiming
- warnings appear before publishing
- risky content can be edited or rejected

### Story 10: Suggest improvement actions
**Priority:** P1  
**Acceptance criteria:**
- suggestions appear like "add proof point" or "tighten hook"
- suggestions are human-readable
- rewrites can be requested from UI

---

## Epic 4: Approval and publishing

### Story 11: Review draft before publishing
**Priority:** P0  
**Acceptance criteria:**
- user sees a single approved draft screen
- can approve, edit, or reject
- edits are saved

### Story 12: Publish or schedule via Publora
**Priority:** P0  
**Acceptance criteria:**
- publish works with LinkedIn publishing API
- schedule works for a chosen time
- result URL is stored

### Story 13: Fallback publishing flow
**Priority:** P1  
**Acceptance criteria:**
- if publish fails, user gets a copy-paste fallback
- error message is clear
- steps are obvious

---

## Epic 5: Beta readiness

### Story 14: Monitoring and alerting
**Priority:** P1  
**Acceptance criteria:**
- critical errors alert team
- API failures visible in dashboard
- service status is monitored

### Story 15: Feedback form and bug tracking
**Priority:** P1  
**Acceptance criteria:**
- beta users can report issues quickly
- bugs are triaged by priority
- fixes are tracked

### Story 16: Release checklist and docs
**Priority:** P0  
**Acceptance criteria:**
- docs exist for beta users
- runbook exists for support
- no critical blocker before launch

---

## Non-functional requirements

### Performance
- generation results in <30 seconds for first MVP
- scoring completes in <5 seconds
- dashboard loads in <3 seconds

### Security
- JWT with refresh logic
- role-based access for org/team features
- no secrets in code
- API keys stored in env vars

### Reliability
- retries for failed generation or publishing calls
- errors visible to user
- no data loss from draft generation

### Observability
- logs for generation flow
- metrics for publish success and failures
- alerts for serious service issues

---

## MVP Done Criteria

The MVP is done when a user can:

- create an account
- build a brand profile
- generate a draft from a prompt
- review safety and score
- approve or edit the draft
- publish it or schedule it

That is the wedge.
