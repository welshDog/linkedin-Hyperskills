from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api import HyperskillsAPI
from src.models import Draft, DraftStatus
from src.storage import DraftStore
from src.workflow import ApprovalEngine

app = FastAPI(
    title="LinkedIn Hyperskills API",
    description="Founder-first AI content operating system for multi-platform publishing",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
api = HyperskillsAPI()
store = DraftStore()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "LinkedIn Hyperskills"}


@app.post("/drafts")
def create_draft(request: dict):
    """Create a new founder draft."""
    try:
        draft = api.create_draft(
            founder_id=request.get("founder_id"),
            title=request.get("title"),
            brief=request.get("brief"),
            platforms=request.get("platforms", ["linkedin"]),
            tags=request.get("tags", []),
            scheduled_for=request.get("scheduled_for"),
            metadata=request.get("metadata", {}),
        )
        store.save_draft(draft)
        return {"status": "created", "draft": draft.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/drafts/{draft_id}")
def get_draft(draft_id: str):
    """Get draft by ID."""
    draft = store.get_draft(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    return {"draft": draft.to_dict()}


@app.get("/drafts")
def list_drafts(founder_id: str = None):
    """List all drafts, optionally filtered by founder."""
    drafts = store.list_drafts(founder_id)
    return {"drafts": [d.to_dict() for d in drafts]}


@app.post("/drafts/{draft_id}/variants")
def add_variant(draft_id: str, request: dict):
    """Add a new variant to a draft."""
    draft = store.get_draft(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    try:
        variant = api.add_variant(draft, request.get("content"))
        store.save_draft(draft)
        return {"status": "added", "variant": variant.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/drafts/{draft_id}/approve/{variant_id}")
def approve_variant(draft_id: str, variant_id: str):
    """Approve a variant for publishing."""
    draft = store.get_draft(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    try:
        approved = api.approve_variant(draft, variant_id)
        store.save_draft(draft)
        return {"status": "approved" if approved else "rejected", "draft": draft.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/drafts/{draft_id}/publish/{variant_id}")
def publish_variant(draft_id: str, variant_id: str):
    """Publish an approved variant to all platforms."""
    draft = store.get_draft(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    try:
        results = api.publish_approved_variant(draft, variant_id)
        store.save_draft(draft)
        return {
            "status": "published",
            "results": [r.to_dict() for r in results],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/drafts/{draft_id}/summary")
def draft_summary(draft_id: str):
    """Get complete draft summary including analytics."""
    draft = store.get_draft(draft_id)
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    return api.get_draft_summary(draft)


@app.get("/campaigns/{founder_id}")
def get_campaign(founder_id: str):
    """Get all drafts for a founder as a campaign."""
    drafts = store.list_drafts(founder_id)
    return {
        "founder_id": founder_id,
        "total_drafts": len(drafts),
        "drafts": [d.to_dict() for d in drafts],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
