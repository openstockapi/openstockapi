from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class MacroIndicatorEntry(BaseModel):
    name: str
    year: int
    period: str  # e.g., "Annual", "Tháng 5/2026"
    value: Optional[float] = None
    unit: str
    source: Optional[str] = None
    provider: str
