# Content scoring heuristics

A lightweight starter for scoring draft quality.

```python
from typing import Dict


class DraftScorer:
    def score(self, text: str) -> Dict:
        cleaned = text.strip()
        sentences = [s for s in cleaned.split(".") if s.strip()]
        words = cleaned.split()

        score = 70

        if len(words) < 60:
            score -= 10

        if len(words) > 500:
            score -= 5

        if len(sentences) > 8:
            score += 5

        if any(token in cleaned.lower() for token in ["leverage", "delve", "unlock", "foster", "fundamentally"]):
            score -= 10

        if any(token in cleaned.lower() for token in ["why", "because", "here’s the truth", "what changed"]):
            score += 5

        score = max(0, min(score, 100))

        return {
            "score": score,
            "summary": "A rough strategic quality score for the draft."
        }
```

This gives a practical starting point for quality and voice checks.
