# 90-Day MVP Build Roadmap

## Strategic focus

We are building ONE wedge:

- brand memory
- draft generation
- claim safety
- approval workflow

Nothing else matters for MVP.

This is the core loop that makes users say: "This actually sounds like me."

---

## Phase 1: Weeks 1-4 — Foundation and auth

### Goal
Get users signed up, authenticated, and able to create their brand profile.

### Week 1: Setup and auth

**Backend:**
- [ ] PostgreSQL schema (users, orgs, basic tables)
- [ ] Node.js + Express API boilerplate
- [ ] Auth service (signup, login, LinkedIn OAuth)
- [ ] JWT token generation and validation
- [ ] Rate limiting

**Frontend:**
- [ ] React app scaffold
- [ ] Auth flow (signup, login)
- [ ] Basic routing
- [ ] Tailwind CSS setup

**DevOps:**
- [ ] Docker compose for local dev
- [ ] GitHub Actions CI/CD pipeline
- [ ] Staging environment
- [ ] Database backups

**Acceptance criteria:**
- [ ] Users can sign up with email
- [ ] Users can log in
- [ ] LinkedIn OAuth works (optional for MVP)
- [ ] JWT tokens validate correctly
- [ ] Rate limiting prevents abuse

### Week 2: Brand profile data model

**Backend:**
- [ ] MongoDB brand_profiles collection
- [ ] Brand profile creation endpoint
- [ ] Brand profile retrieval endpoint
- [ ] Brand profile update endpoint
- [ ] Sample data fixtures

**Frontend:**
- [ ] Brand profile form (initial)
- [ ] Post upload UI (drag and drop or paste)
- [ ] Basic styling

**Acceptance criteria:**
- [ ] Brand profile can be created and stored
- [ ] All fields persist correctly
- [ ] Users can update their profile
- [ ] Profiles are user-specific and isolated

### Week 3: Voice extraction (MVP version)

**Backend:**
- [ ] Simple voice profile extractor
  - Extract top phrases
  - Detect tone (heuristic-based)
  - Identify banned phrases user mentions
  - Build audience definition
- [ ] POST /brand/extract-voice endpoint
- [ ] Voice profile stored in MongoDB

**Frontend:**
- [ ] Upload sample posts UI
- [ ] Display extracted voice profile
- [ ] Allow user to edit extracted voice
- [ ] Save refined profile

**Implementation hint:**
```python
# Simple extraction heuristic
def extract_voice(posts):
    all_text = " ".join(posts)
    sentences = all_text.split(".")
    
    # Tone detection
    tone = "conversational" if "I" in all_text else "professional"
    
    # Key phrases (frequency-based)
    words = all_text.lower().split()
    key_phrases = [w for w in words if len(w) > 5][:10]
    
    # Banned phrases (common AI tells)
    banned = []
    for phrase in ["leverage", "synergy", "fundamentally"]:
        if phrase in all_text.lower():
            banned.append(phrase)
    
    return {
        "tone": tone,
        "key_phrases": key_phrases,
        "banned_phrases": banned,
        "audience": "infer from posts"
    }
```

**Acceptance criteria:**
- [ ] Voice extraction works for 5-10 sample posts
- [ ] Extracted tone is reasonable
- [ ] Key phrases are captured
- [ ] Users can review and edit
- [ ] Profile saved to MongoDB

### Week 4: Polish and prepare for generation

**Backend:**
- [ ] Add voice profile to cache (Redis)
- [ ] Optimize profile retrieval
- [ ] Add error handling
- [ ] Write tests for auth and brand profile
- [ ] Documentation for brand profile schema

**Frontend:**
- [ ] Better onboarding flow
- [ ] Profile preview page
- [ ] Navigation between sections
- [ ] Error messaging

**Testing:**
- [ ] Unit tests for backend services
- [ ] Integration tests for auth flow
- [ ] Manual testing checklist

**Acceptance criteria:**
- [ ] All Phase 1 features working end-to-end
- [ ] No critical bugs
- [ ] Performance acceptable
- [ ] Ready for internal testing

---

## Phase 2: Weeks 5-7 — Draft generation and scoring

### Goal
Users can request a post and get back 2-3 scored drafts in their voice.

### Week 5: Content generation service

**Backend:**
- [ ] Python FastAPI service for generation
- [ ] Claude API integration
- [ ] Prompt engineering layer
  - Brand memory context
  - Topic brief handling
  - Voice injection into prompt
  - Multiple variant generation
- [ ] Queue system (Celery + Redis) for async jobs
- [ ] Generation endpoint: POST /content/generate
- [ ] Webhook for completion

**Prompt template (starter):**
```
You are writing a LinkedIn post for {name}.

Their positioning: {positioning}
Their tone: {tone}
Their audience: {audience}
Key phrases they use: {key_phrases}
Avoid: {banned_phrases}

Write 3 variants of a LinkedIn post about: {topic}

Each variant should:
- Sound authentic, not like AI
- Be 900-1300 characters
- Include a clear hook
- Have a CTA
- Stay true to their voice

Return as JSON: {"variants": [{"text": "...", "hook_type": "..."}]}
```

**Frontend:**
- [ ] Content generation form
- [ ] Topic/brief input
- [ ] Mode selector (founder, operator, basic)
- [ ] Loading state
- [ ] Display 2-3 variants

**Acceptance criteria:**
- [ ] Generation works end-to-end
- [ ] Drafts complete in <30 seconds
- [ ] Multiple variants generated
- [ ] Variants are different
- [ ] Quality is reasonable (hand-tested)

### Week 6: Scoring and claim safety

**Backend:**
- [ ] Content scoring service (Python)
- [ ] Scoring algorithm (see technical data model)
  - Clarity score
  - Originality score
  - Hook strength score
  - CTA clarity score
  - Trust level score
- [ ] Claim safety checker
  - Flag risky language
  - Suggest rewrites
  - Show risk level (low/medium/high)
- [ ] POST /score/content endpoint
- [ ] POST /safety/check-claims endpoint

**Scoring implementation:**
```python
class ContentScorer:
    def score(self, text):
        scores = {
            "clarity": self.score_clarity(text),
            "originality": self.score_originality(text),
            "hook_strength": self.score_hook(text),
            "cta_clarity": self.score_cta(text),
            "trust": self.score_trust(text)
        }
        scores["overall"] = sum(scores.values()) / 5
        return scores
    
    def score_clarity(self, text):
        # Penalize long sentences, reward short ones
        sentences = text.split(".")
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        if 10 < avg_length < 20:
            return 25
        return 20
    
    def score_hook(self, text):
        # Check if starts with strong opening
        hooks = ["why", "what", "when", "here's", "nobody"]
        first_word = text.split()[0].lower()
        if any(first_word.startswith(h) for h in hooks):
            return 20
        return 10
    # ... more scoring methods
```

**Frontend:**
- [ ] Score display (visual breakdown)
- [ ] Claim safety flags (highlighted)
- [ ] Improvement suggestions
- [ ] Side-by-side draft comparison

**Acceptance criteria:**
- [ ] Scoring completes in <5 seconds
- [ ] Scores make intuitive sense
- [ ] Claim flags catch obvious risks
- [ ] Users can understand scores

### Week 7: Integration and polish

**Backend:**
- [ ] Connect generation → scoring pipeline
- [ ] Store scores with posts in MongoDB
- [ ] Optimize for speed
- [ ] Error handling and retries
- [ ] Logging for debugging

**Frontend:**
- [ ] Full end-to-end flow
- [ ] Draft review page
- [ ] Score explanation tooltips
- [ ] UX polish
- [ ] Mobile responsiveness

**Testing:**
- [ ] Generation quality tests (hand-reviewed)
- [ ] Scoring consistency tests
- [ ] Safety flag accuracy tests
- [ ] Performance benchmarks

**Acceptance criteria:**
- [ ] Users can go from brief to scored draft
- [ ] Whole flow takes <2 minutes
- [ ] Quality is high enough to show to users
- [ ] No major bugs

---

## Phase 3: Weeks 8-9 — Approval workflow and publishing

### Goal
Users can approve drafts and publish them (or schedule for later).

### Week 8: Approval workflow

**Backend:**
- [ ] posts table schema
- [ ] POST /posts/create (from approved draft)
- [ ] PUT /posts/{postId}/approve
- [ ] PUT /posts/{postId}/reject
- [ ] PUT /posts/{postId}/edit
- [ ] GET /posts (user's posts)
- [ ] POST /posts/{postId}/publish-now
- [ ] POST /posts/{postId}/schedule

**Frontend:**
- [ ] Approval decision UI
- [ ] Edit draft inline
- [ ] Request rewrites (send back to generation)
- [ ] Publish or schedule options
- [ ] Posts dashboard (pending, published)

**Database updates:**
- [ ] posts table with status tracking
- [ ] Schedule field for future posts
- [ ] Published URL storage

**Acceptance criteria:**
- [ ] Users can approve/reject drafts
- [ ] Users can edit before publishing
- [ ] Status tracking works
- [ ] Workflow is clear and simple

### Week 9: Publishing integration (MVP version)

**Backend:**
- [ ] Simple Publora integration
- [ ] POST /publish/create-draft (creates draft on LinkedIn)
- [ ] POST /publish/schedule (schedules for later)
- [ ] Handle Publora API errors gracefully
- [ ] Store Publora response (post ID, URL)

**Frontend:**
- [ ] Copy-paste fallback (if Publora fails)
- [ ] Schedule picker (date/time)
- [ ] Confirmation before publish
- [ ] Published post link

**Fallback:**
- [ ] If Publora fails, show raw post for copy-paste
- [ ] Clear instructions

**Acceptance criteria:**
- [ ] At least 80% of posts publish successfully
- [ ] Scheduled posts work
- [ ] Fallback (copy-paste) is clear
- [ ] No lost posts

---

## Phase 4: Week 10 — Polish, testing, and readiness

### Goal
MVP is production-ready for beta launch.

### Testing sprint

**Manual testing:**
- [ ] End-to-end user flow (10+ times)
- [ ] Edge cases (empty posts, very long text, special characters)
- [ ] Error handling (network down, API failures)
- [ ] Performance (load under concurrent users)
- [ ] Security (auth, data isolation, SQL injection)

**Automated testing:**
- [ ] Unit tests for all services (target: 70%+ coverage)
- [ ] Integration tests for critical flows
- [ ] API contract tests
- [ ] Database tests

**Bug fixes:**
- [ ] Triage and fix all P1 and P2 bugs
- [ ] Test fixes thoroughly

### Optimization

- [ ] Database query optimization
- [ ] Cache layer (Redis) for brand profiles
- [ ] Frontend performance (lazy loading, code splitting)
- [ ] API response time <500ms target

### Documentation

- [ ] User guide for beta testers
- [ ] API documentation
- [ ] Database schema documentation
- [ ] Deployment runbook
- [ ] Troubleshooting guide

### Launch preparation

- [ ] Prepare beta user invitations
- [ ] Set up monitoring and alerting
- [ ] Create feedback form
- [ ] Prepare support template responses
- [ ] Create onboarding video (2 min)

**Acceptance criteria:**
- [ ] All critical features working
- [ ] No known critical bugs
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] Ready for 50-100 beta users

---

## Success metrics by phase

### Phase 1 (Weeks 1-4)
- [ ] All auth endpoints working
- [ ] Brand profiles can be created and retrieved
- [ ] Voice extraction produces reasonable results
- [ ] Internal testing passes

### Phase 2 (Weeks 5-7)
- [ ] Generation quality acceptable (hand-tested)
- [ ] Scoring correlates with quality
- [ ] Safety flags catch obvious issues
- [ ] End-to-end flow <2 minutes

### Phase 3 (Weeks 8-9)
- [ ] Approval workflow is intuitive
- [ ] Publishing success rate >80%
- [ ] No lost posts
- [ ] Scheduling works reliably

### Phase 4 (Week 10)
- [ ] All tests passing
- [ ] <5 P1 bugs
- [ ] API response time <500ms
- [ ] Documentation complete
- [ ] Ready for public beta

---

## Technology stack (final)

### Backend
- Node.js + Express (auth, API)
- Python + FastAPI (generation, scoring, safety)
- PostgreSQL (users, orgs, posts)
- MongoDB (brand profiles, drafts)
- Redis (cache, sessions)
- Celery + Redis (job queue)

### Frontend
- React
- Tailwind CSS
- React Query (data fetching)
- Zustand (state)

### Integrations
- Claude API (generation)
- Publora API (publishing)
- LinkedIn OAuth (auth)

### DevOps
- Docker + Docker Compose
- GitHub Actions
- AWS (EC2, RDS, S3)
- Datadog (monitoring)

---

## Team structure for this build

**Required roles:**
- Backend engineer (Node.js) — auth, API
- Backend engineer (Python) — generation, scoring
- Frontend engineer (React) — UI, flows
- Product manager — prioritization, decisions
- Content strategist — prompts, voice, playbooks

**Optional but helpful:**
- DevOps engineer (can start Week 5)
- QA/tester (can start Week 8)

---

## Risk and contingency

### Risk: Claude API quality is poor
**Mitigation:**
- Heavy prompt engineering
- Test multiple prompts
- Consider fallback to GPT-4 if needed
- Manual curation of early outputs

### Risk: Publora API has issues
**Mitigation:**
- Copy-paste fallback (always available)
- Keep it simple (schedule + publish only)
- Test thoroughly in Week 9
- Have Publora support contact ready

### Risk: We miss timeline
**Mitigation:**
- Ruthless scope cutting if needed
- Drop features, not quality
- Phase 3 (publishing) can be manual if needed
- Phase 4 (analytics) comes later

### Risk: Low user engagement during beta
**Mitigation:**
- Pick power-user beta testers
- Daily feedback loops
- Fast iteration on feedback
- Weekly check-ins with top users

---

## What we're NOT building (MVP scope)

- Analytics and engagement tracking
- Campaign orchestration
- Team collaboration
- Founder playbook modes (start simple)
- Image generation (Pixfaro integration)
- Advanced brand memory tuning
- A/B testing
- API access
- White-label options

We add these after MVP traction.

---

## What happens after Week 10

Once MVP is in beta:

**Weeks 11-12:** Beta feedback sprint
- Run with 50-100 beta users
- Daily monitoring
- Fast bug fixes
- Weekly feature iterations
- Collect testimonials

**Week 13+:** Public beta launch
- Open to wider audience
- Prepare launch materials
- Begin growth initiatives

---

**The goal: By end of Week 10, we have a product that makes users say: "This actually sounds like me, and it's way faster than writing it myself."**

Everything else follows from that.
