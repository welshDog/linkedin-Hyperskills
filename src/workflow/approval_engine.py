from __future__ import annotations

from typing import Dict

from src.claim_safety import ClaimSafetyChecker
from src.content_score import DraftScorer
from src.models import Draft, DraftStatus, Variant


class ApprovalEngine:
    """Orchestrates the scoring and approval workflow for a draft."""

    def __init__(self) -> None:
        self.scorer = DraftScorer()
        self.safety_checker = ClaimSafetyChecker()

    def score_variant(self, variant: Variant) -> None:
        """Run quality scoring on a variant."""
        score_result = self.scorer.score(variant.content)
        variant.score = score_result.get("score", 0)

    def check_claims(self, variant: Variant) -> None:
        """Run claim safety check on a variant."""
        safety_result = self.safety_checker.evaluate(variant.content)
        variant.claim_risk = safety_result.get("risk", "low")

    def approve_workflow(self, draft: Draft, variant_id: str) -> bool:
        """
        Full approval workflow:
        1. Score the variant
        2. Check claims
        3. Mark as approved if risk is acceptable
        """
        variant = None
        for v in draft.variants:
            if v.variant_id == variant_id:
                variant = v
                break

        if not variant:
            return False

        # Score the variant
        draft.set_status(DraftStatus.SCORING)
        self.score_variant(variant)

        # Check claims
        draft.set_status(DraftStatus.SAFETY_CHECK)
        self.check_claims(variant)

        # If high risk, flag the draft
        if variant.claim_risk == "high":
            draft.set_status(DraftStatus.FLAGGED)
            return False

        # Otherwise approve
        draft.set_status(DraftStatus.SCORED)
        draft.approve_variant(variant_id)
        return True

    def get_approval_summary(self, draft: Draft) -> Dict[str, any]:
        """Get a summary of the approval status for all variants."""
        return {
            "draft_id": draft.draft_id,
            "status": draft.status.value,
            "variants": [
                {
                    "variant_id": v.variant_id,
                    "score": v.score,
                    "claim_risk": v.claim_risk,
                    "approved": v.approved,
                }
                for v in draft.variants
            ],
        }


__all__ = ["ApprovalEngine"]
