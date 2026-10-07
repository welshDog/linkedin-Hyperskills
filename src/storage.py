from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

import json

from src.models import Draft, DraftStatus, Variant


@dataclass
class DraftStore:
    """Persist drafts to JSON files."""

    storage_dir: Path = Path("./data/drafts")

    def __post_init__(self):
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, draft_id: str) -> Path:
        return self.storage_dir / f"{draft_id}.json"

    def save_draft(self, draft: Draft) -> None:
        """Save draft to JSON file."""
        path = self._get_path(draft.draft_id)
        with open(path, "w") as f:
            json.dump(draft.to_dict(), f, indent=2)

    def get_draft(self, draft_id: str) -> Optional[Draft]:
        """Load draft from JSON file."""
        path = self._get_path(draft_id)
        if not path.exists():
            return None
        with open(path, "r") as f:
            data = json.load(f)
        return self._dict_to_draft(data)

    def list_drafts(self, founder_id: Optional[str] = None) -> List[Draft]:
        """List all drafts, optionally filtered by founder."""
        drafts = []
        for path in self.storage_dir.glob("*.json"):
            with open(path, "r") as f:
                data = json.load(f)
            if founder_id and data.get("founder_id") != founder_id:
                continue
            drafts.append(self._dict_to_draft(data))
        return drafts

    def _dict_to_draft(self, data: Dict) -> Draft:
        """Reconstruct Draft object from JSON dict."""
        variants = [
            Variant(
                content=v["content"],
                variant_id=v["variant_id"],
                created_at=v["created_at"],
                score=v.get("score"),
                claim_risk=v.get("claim_risk"),
                approved=v.get("approved", False),
                approved_at=v.get("approved_at"),
            )
            for v in data.get("variants", [])
        ]
        return Draft(
            founder_id=data["founder_id"],
            title=data["title"],
            brief=data["brief"],
            platforms=data.get("platforms", []),
            variants=variants,
            status=DraftStatus(data.get("status", "created")),
            draft_id=data["draft_id"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            tags=data.get("tags", []),
            scheduled_for=data.get("scheduled_for"),
            metadata=data.get("metadata", {}),
        )


__all__ = ["DraftStore"]
