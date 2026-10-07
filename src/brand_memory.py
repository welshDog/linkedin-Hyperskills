# Brand memory model

This is a starter model for storing a user’s content profile.

```python
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class BrandProfile:
    name: str
    audience: str
    positioning: str
    tone: str
    values: List[str] = field(default_factory=list)
    banned_phrases: List[str] = field(default_factory=list)
    proof_points: List[str] = field(default_factory=list)
    strong_hooks: List[str] = field(default_factory=list)
    weak_signals: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "audience": self.audience,
            "positioning": self.positioning,
            "tone": self.tone,
            "values": self.values,
            "banned_phrases": self.banned_phrases,
            "proof_points": self.proof_points,
            "strong_hooks": self.strong_hooks,
            "weak_signals": self.weak_signals,
        }
```

This is intentionally lightweight and extensible.
