from dataclasses import dataclass
from typing import Optional, Literal

Reason = Optional[Literal["not_found", "conflict", "ok"]]

@dataclass
class UpdateResult:
    affected_rows: int
    item: Optional[dict]
    reason: Reason = None