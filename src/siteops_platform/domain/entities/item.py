"""Domain entity (pure Python)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Item:
    id: uuid.UUID
    name: str
    created_at: Optional[datetime] = None