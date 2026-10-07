# App architecture spec

## System overview

LinkedIn Hyperskills is a cloud-native, event-driven SaaS platform built on microservices architecture.

The system is designed for:
- High availability
- Scalability
- Real-time analytics
- Low latency for content generation
- Secure API integrations

## Architecture diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Web App     │  │  Desktop App │  │  Mobile (future) │  │
│  │  (React)     │  │  (Electron)  │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  API Gateway│
                    │  (Auth, Rate│
                    │   Limiting) │
                    └──────┬──────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                     Service Layer                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Auth &     │  │   Content    │  │   Publishing     │  │
│  │   User Mgmt  │  │   Generation │  │   Service        │  │
│  │   Service    │  │   Service    │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Scoring &   │  │  Analytics   │  │   Brand Memory   │  │
│  │  Safety      │  │   Service    │  │   Service        │  │
│  │  Service     │  │              │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│                   Data Layer                                │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  PostgreSQL  │  │   MongoDB    │  │  TimescaleDB     │  │
│  │  (Users,     │  │  (Profiles,  │  │  (Analytics,     │  │
│  │   Teams,     │  │   Content)   │  │   Engagement)    │  │
│  │   Billing)   │  │              │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │  Redis Cache │  │  S3 Storage  │                         │
│  │  (Sessions,  │  │  (Posts,     │                         │
│  │   Cache)     │  │   Media)     │                         │
│  └──────────────┘  └──────────────┘                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┴──────────────────────────────────┐
│              External Integrations                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Claude API  │  │  Publora     │  │  LinkedIn OAuth  │  │
│  │  (Generation)│  │  (Publishing)│  │  (Auth)          │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Apify       │  │  Pixfaro     │  │  Stripe          │  │
│  │  (Read data) │  │  (Images)    │  │  (Billing)       │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Service definitions

### 1. Auth & User Management Service

**Responsibility:**
- User signup, login, password management
- LinkedIn OAuth integration
- Team and org management
- Permissions and role-based access control (RBAC)

**Tech stack:**
- Node.js + Express or Python + FastAPI
- PostgreSQL for user data
- Redis for session storage

**API endpoints:**
- POST /auth/signup
- POST /auth/login
- POST /auth/logout
- GET /auth/me
- POST /orgs
- GET /orgs/{orgId}/users

---

### 2. Content Generation Service

**Responsibility:**
- Accept user brief + brand memory
- Generate drafts via Claude API
- Support multiple modes (founder, operator, builder)
- Handle rewrites and variations

**Tech stack:**
- Python + FastAPI (best for AI integration)
- Claude API (via Anthropic SDK)
- Prompt engineering layer
- Queue system (Celery + Redis) for async jobs

**API endpoints:**
- POST /content/generate
- POST /content/rewrite
- GET /content/{contentId}
- POST /content/{contentId}/approve

**Processing flow:**
1. User submits brief
2. Service fetches brand memory
3. System constructs prompt with context
4. Claude generates 2-3 variants
5. Results stored in MongoDB
6. Callback to frontend

---

### 3. Scoring & Safety Service

**Responsibility:**
- Score drafts on quality, originality, clarity
- Flag claim-safety issues
- Detect AI tell density
- Provide improvement suggestions

**Tech stack:**
- Python + FastAPI
- Heuristic-based scoring (initially)
- NLP libraries (spaCy, TextBlob)
- Optional: fine-tuned classifier for claim detection

**API endpoints:**
- POST /score/content
- POST /safety/check-claims
- GET /safety/guidelines

**Scoring model:**
- Clarity (word choice, sentence length): 0-25 points
- Originality (uniqueness vs. archive): 0-25 points
- Hook strength (engagement pull): 0-20 points
- CTA clarity (next step): 0-15 points
- Trust level (claim verification): 0-15 points

---

### 4. Brand Memory Service

**Responsibility:**
- Store and retrieve user voice profiles
- Extract voice from sample posts
- Update profiles from published content
- Manage audience definitions and proof points

**Tech stack:**
- Python + FastAPI
- MongoDB (flexible schema for profiles)
- Embedding vectors (optional, for semantic search)

**API endpoints:**
- POST /brand/profile
- GET /brand/profile/{userId}
- PUT /brand/profile/{userId}
- POST /brand/extract-voice (from samples)

**Profile structure:**
```json
{
  "userId": "...",
  "voice": {
    "tone": "...",
    "vocabulary": [...],
    "sentence_patterns": [...]
  },
  "positioning": {
    "title": "...",
    "audience": "...",
    "values": [...]
  },
  "proof_points": [...],
  "banned_phrases": [...],
  "success_patterns": [...]
}
```

---

### 5. Publishing Service

**Responsibility:**
- Handle approval workflow
- Schedule posts
- Integrate with Publora for publishing
- Manage media uploads (Pixfaro, S3)
- Support post variants and A/B testing

**Tech stack:**
- Node.js + Express
- PostgreSQL for scheduling
- Redis for job queue
- Publora API client
- S3 for media storage

**API endpoints:**
- POST /publish/schedule
- PUT /publish/{postId}/approve
- DELETE /publish/{postId}
- POST /publish/{postId}/publish-now
- GET /publish/calendar

---

### 6. Analytics Service

**Responsibility:**
- Ingest engagement data from LinkedIn (via Apify)
- Tag posts by hook type, format, topic
- Track performance trends
- Generate recommendations
- Provide dashboards and reports

**Tech stack:**
- Python + FastAPI
- TimescaleDB or ClickHouse (time-series analytics)
- Apify client for LinkedIn data
- Analytics aggregation layer

**API endpoints:**
- POST /analytics/ingest-engagement
- GET /analytics/top-posts
- GET /analytics/hook-performance
- GET /analytics/trends
- GET /analytics/recommendations

**Data model:**
```
post_metrics:
  - post_id
  - hook_type
  - format (single, carousel, thread)
  - topic_category
  - published_at
  - engagement_rate
  - likes, comments, shares, saves
  - conversion_signal (if available)
```

---

### 7. Webhook Receiver (Events)

**Responsibility:**
- Receive LinkedIn engagement updates
- Trigger analytics ingestion
- Handle Stripe webhooks for billing events
- Queue async tasks

**Tech stack:**
- Node.js + Express
- Webhook signature verification
- Event routing to appropriate services

---

## Data flow

### Content generation flow

```
User brief
    ↓
Content Generation Service
    ├─ Fetch brand memory
    ├─ Construct prompt
    ├─ Call Claude API
    ├─ Generate 2-3 variants
    ↓
Scoring & Safety Service
    ├─ Score each draft
    ├─ Check claims
    ├─ Flag risks
    ↓
Return scored drafts to frontend
    ↓
User reviews and approves
    ↓
Publishing Service
    ├─ Store in database
    ├─ Schedule via Publora
    ↓
Post published on LinkedIn
    ↓
Analytics Service
    ├─ Poll LinkedIn via Apify
    ├─ Ingest engagement
    ├─ Tag and categorize
    ├─ Learn patterns
    ↓
Recommendations for next posts
```

## Deployment architecture

### Infrastructure

- **Cloud platform:** AWS or Google Cloud
- **Container orchestration:** Kubernetes (EKS/GKE)
- **Service mesh:** Istio (optional, for advanced routing)
- **CI/CD:** GitHub Actions or GitLab CI
- **Monitoring:** Datadog or New Relic
- **Logging:** ELK stack or Datadog

### Deployment pipeline

```
Git push to main
    ↓
GitHub Actions
    ├─ Run tests
    ├─ Build Docker images
    ├─ Push to ECR
    ↓
Deploy to staging
    ├─ Automated tests
    ├─ Smoke tests
    ↓
Manual approval for production
    ↓
Deploy to production
    ├─ Blue-green deployment
    ├─ Health checks
    ├─ Rollback if needed
```

## Security

### Authentication
- OAuth 2.0 for LinkedIn integration
- JWT tokens for internal APIs
- Session management with Redis

### Authorization
- Role-based access control (RBAC)
- Team and org-level permissions
- API key management for integrations

### Data protection
- HTTPS/TLS for all traffic
- Encryption at rest (RDS, MongoDB)
- Encryption in transit
- Secrets management (Vault or AWS Secrets Manager)

### Compliance
- GDPR compliance
- Data retention policies
- Audit logging
- Regular security audits

## Scalability

### Horizontal scaling
- All services deployed as multiple replicas
- Load balancing across instances
- Auto-scaling based on CPU/memory/request rate

### Database scaling
- PostgreSQL read replicas for scaling reads
- Sharding strategy for large datasets (future)
- TimescaleDB for time-series data (already horizontally scalable)

### Caching
- Redis for session storage
- Application-level caching for brand profiles
- CDN for static assets

## Performance targets

- API response time: <500ms for 95th percentile
- Content generation: <30 seconds
- Scoring: <5 seconds
- Analytics queries: <2 seconds
- Publish scheduling: <1 second

## Monitoring and observability

### Metrics
- API latency and throughput
- Error rates and types
- Service health
- Database performance
- Claude API costs and usage

### Logging
- Structured JSON logging
- Request tracing across services
- Debug logging for troubleshooting

### Alerting
- High error rates
- Service downtime
- Database issues
- API rate limit approaching

## Development workflow

### Local development
```bash
# Run all services locally with Docker Compose
docker-compose up

# Access services
- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000
- Services on various ports
```

### Testing
- Unit tests for each service
- Integration tests for API flows
- End-to-end tests for critical user journeys
- Load testing for performance validation

---

**This architecture supports:**
- Fast iteration during MVP phase
- Scaling to production traffic
- Multiple product tiers and features
- Third-party integrations
- Real-time analytics
- Security and compliance
