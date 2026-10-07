# Claim safety heuristics

A simple starter evaluator for risk-prone content.

```python
from typing import List, Dict


class ClaimSafetyChecker:
    def __init__(self):
        self.risky_keywords = [
            "guaranteed",
            "#1",
            "best in class",
            "instant",
            "viral",
            "unbeatable",
            "100%",
        ]

    def evaluate(self, text: str) -> Dict:
        lowered = text.lower()
        hits = [keyword for keyword in self.risky_keywords if keyword in lowered]

        risk = "low"
        if hits:
            risk = "medium"

        if any(word in lowered for word in ["guaranteed results", "100% increase", "always wins"]):
            risk = "high"

        return {
            "risk": risk,
            "hits": hits,
            "message": "Claim language should be checked against proof and audience context."
        }
```

This is not a legal verifier. It is a strong early-warning system.
