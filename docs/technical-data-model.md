# Technical data model

## Database schema overview

### PostgreSQL (Users, Teams, Billing, Publishing)

#### users table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    linkedin_id VARCHAR(255),
    linkedin_access_token TEXT,
    linkedin_refresh_token TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    subscription_tier VARCHAR(50) DEFAULT 'free'
);
```

#### orgs table
```sql
CREATE TABLE orgs (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    billing_email VARCHAR(255),
    stripe_customer_id VARCHAR(255)
);
```

#### org_members table
```sql
CREATE TABLE org_members (
    id UUID PRIMARY KEY,
    org_id UUID REFERENCES orgs(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50), -- owner, admin, member
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(org_id, user_id)
);
```

#### posts table
```sql
CREATE TABLE posts (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    org_id UUID REFERENCES orgs(id) ON DELETE CASCADE,
    title VARCHAR(255),
    content TEXT NOT NULL,
    status VARCHAR(50), -- draft, approved, published, scheduled
    hook_type VARCHAR(100),
    format VARCHAR(50), -- single, carousel, thread
    topic_category VARCHAR(100),
    content_mode VARCHAR(50), -- founder, operator, builder
    score_overall INT,
    score_clarity INT,
    score_originality INT,
    score_hook INT,
    score_cta INT,
    score_trust INT,
    claim_safety_risk VARCHAR(50), -- low, medium, high
    claim_flags JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    scheduled_at TIMESTAMP,
    published_at TIMESTAMP,
    published_url VARCHAR(500),
    linkedin_post_urn VARCHAR(255)
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_org_id ON posts(org_id);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_published_at ON posts(published_at);
```

#### post_engagement table
```sql
CREATE TABLE post_engagement (
    id UUID PRIMARY KEY,
    post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT NOW(),
    likes INT DEFAULT 0,
    comments INT DEFAULT 0,
    shares INT DEFAULT 0,
    saves INT DEFAULT 0,
    engagement_rate FLOAT,
    impressions INT,
    clicks INT,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### billing_events table
```sql
CREATE TABLE billing_events (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    org_id UUID REFERENCES orgs(id),
    event_type VARCHAR(100), -- subscription_created, subscription_updated, charge_succeeded
    stripe_event_id VARCHAR(255) UNIQUE,
    amount INT,
    currency VARCHAR(10),
    stripe_subscription_id VARCHAR(255),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

### MongoDB (Brand Profiles, Content Metadata)

#### brand_profiles collection
```json
{
  "_id": ObjectId,
  "user_id": "uuid",
  "org_id": "uuid",
  "name": "string",
  "positioning": {
    "title": "string",
    "headline": "string",
    "audience": "string",
    "audience_segments": ["founder", "operator", ...],
    "key_values": ["authenticity", "transparency", ...],
    "unique_angle": "string"
  },
  "voice": {
    "tone": "string", -- conversational, professional, casual
    "key_phrases": ["string"],
    "banned_phrases": ["string"],
    "sentence_patterns": {
      "avg_length": "number",
      "punctuation_style": "string",
      "examples": ["string"]
    },
    "vocabulary_level": "string" -- academic, professional, casual
  },
  "proof_points": [
    {
      "claim": "string",
      "evidence": "string",
      "metrics": ["string"],
      "verified": "boolean"
    }
  ],
  "success_patterns": {
    "best_hooks": ["string"],
    "best_formats": ["string"],
    "best_topics": ["string"],
    "best_posting_times": ["string"],
    "conversion_signals": ["string"]
  },
  "content_modes": {
    "founder": {
      "hooks": ["string"],
      "structure": "string",
      "cta_style": "string"
    },
    "operator": { ... },
    "builder": { ... }
  },
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "last_updated_from_post": "timestamp"
}
```

#### content_drafts collection
```json
{
  "_id": ObjectId,
  "post_id": "uuid",
  "user_id": "uuid",
  "content": "string",
  "metadata": {
    "hook_type": "string",
    "format": "string",
    "topic_category": "string",
    "content_mode": "string",
    "generation_prompt": "string",
    "model_used": "string",
    "tokens_used": "number",
    "cost": "number"
  },
  "scores": {
    "overall": "number",
    "clarity": "number",
    "originality": "number",
    "hook_strength": "number",
    "cta_clarity": "number",
    "trust_level": "number"
  },
  "safety_check": {
    "risk_level": "string",
    "flags": [
      {
        "type": "string",
        "text": "string",
        "suggestion": "string"
      }
    ],
    "overall_assessment": "string"
  },
  "created_at": "timestamp",
  "approved_at": "timestamp"
}
```

---

### TimescaleDB (Analytics, Time-Series Data)

#### post_metrics table (hypertable)
```sql
CREATE TABLE post_metrics (
    time TIMESTAMP NOT NULL,
    post_id UUID NOT NULL,
    user_id UUID NOT NULL,
    org_id UUID NOT NULL,
    hook_type VARCHAR(100),
    format VARCHAR(50),
    topic_category VARCHAR(100),
    content_mode VARCHAR(50),
    likes INT,
    comments INT,
    shares INT,
    saves INT,
    impressions INT,
    clicks INT,
    engagement_rate FLOAT,
    conversion_signal BOOLEAN
);

SELECT create_hypertable('post_metrics', 'time', if_not_exists => TRUE);

CREATE INDEX idx_post_metrics_user ON post_metrics(user_id, time DESC);
CREATE INDEX idx_post_metrics_org ON post_metrics(org_id, time DESC);
CREATE INDEX idx_post_metrics_hook ON post_metrics(hook_type, time DESC);
```

#### engagement_hourly (materialized view)
```sql
CREATE MATERIALIZED VIEW engagement_hourly AS
SELECT 
    time_bucket('1 hour', time) AS hour,
    user_id,
    org_id,
    hook_type,
    COUNT(*) AS post_count,
    AVG(engagement_rate) AS avg_engagement,
    MAX(likes) AS max_likes,
    MAX(comments) AS max_comments
FROM post_metrics
GROUP BY hour, user_id, org_id, hook_type;
```

---

### Redis (Cache, Sessions, Queues)

#### Session storage
```
Key: session:{sessionId}
Value: {
  userId: string,
  orgId: string,
  email: string,
  permissions: [string]
}
TTL: 24 hours
```

#### Brand profile cache
```
Key: brand_profile:{userId}
Value: (JSON serialized brand profile)
TTL: 12 hours
```

#### Content generation queue
```
Key: queue:generation
Value: List of job objects with:
  - jobId
  - userId
  - brief
  - timestamp
  - status
```

#### Rate limiting
```
Key: ratelimit:{userId}:{endpoint}
Value: request count
TTL: 1 hour
```

---

### S3 (Media storage)

#### Bucket structure
```
s3://hyperskills-storage/
├── posts/
│   ├── {userId}/
│   │   ├── {postId}/
│   │   │   ├── original.md
│   │   │   ├── featured_image.jpg
│   │   │   └── carousel_slides/
│   │   │       ├── slide_1.jpg
│   │   │       └── slide_2.jpg
├── avatars/
│   ├── {userId}/avatar.jpg
├── exports/
│   ├── {userId}/
│   │   └── monthly_report_{month}.pdf
```

---

## Data relationships

```
users (1) ──── (M) orgs
   │
   └──── (M) posts
           │
           ├──── (1) brand_profiles
           ├──── (M) post_engagement
           ├──── (M) content_drafts
           └──── (M) post_metrics (TimescaleDB)

orgs (1) ──── (M) org_members
  │
  └──── (M) posts
         └──── (M) billing_events
```

---

## Data consistency and transactions

### Critical transactions

1. **Post creation and scoring**
   - Create post record
   - Store content draft in MongoDB
   - Run scoring
   - Update post with scores
   - All in single transaction

2. **Publishing workflow**
   - Mark post as approved
   - Create publishing job
   - Call Publora API
   - Update post status and URL
   - Rollback if Publora fails

3. **Engagement ingestion**
   - Fetch new engagement from LinkedIn
   - Update post_engagement table
   - Trigger TimescaleDB insert
   - Recalculate user analytics

---

## Performance considerations

### Indexing strategy

**PostgreSQL:**
- Composite indexes on (user_id, status) for filtering
- Index on published_at for time-range queries
- Index on linkedin_post_urn for external lookups

**MongoDB:**
- Index on user_id and org_id
- Index on created_at for sorting

**TimescaleDB:**
- Automatic indexes on (user_id, time)
- Chunk-aware queries for efficiency

### Query optimization

- Use materialized views for common analytics queries
- Cache frequently accessed brand profiles in Redis
- Denormalize engagement data for faster reads
- Use pagination for large result sets

---

## Backup and disaster recovery

### Backup strategy

- PostgreSQL: Daily automated backups, 30-day retention
- MongoDB: Continuous replication, daily snapshots
- TimescaleDB: Automated backups, 7-day retention
- S3: Versioning enabled, cross-region replication

### RTO/RPO targets

- Recovery Time Objective (RTO): 1 hour
- Recovery Point Objective (RPO): 15 minutes

---

## Data retention and privacy

### Retention policies

- User data: Kept until account deletion
- Posts: Kept indefinitely (user can delete)
- Engagement metrics: Kept for 2 years
- Logs: Kept for 30 days
- Backups: Kept for 30 days

### GDPR compliance

- Right to access: Export all user data
- Right to deletion: Delete account and all associated data
- Data portability: Export posts and analytics
- Audit logging: Track all data access

---

This data model supports:
- Multi-tenant architecture
- Scalability to millions of posts and users
- Real-time analytics
- Compliance and security
- Fast access to frequently used data
