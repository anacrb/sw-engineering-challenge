from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RentStatus(str, Enum):
    CREATED = "CREATED"
    WAITING_DROPOFF = "WAITING_DROPOFF"
    WAITING_PICKUP = "WAITING_PICKUP"
    DELIVERED = "DELIVERED"


class RentSize(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"


class Rent(BaseModel):
    id: str
    lockerId: str
    weight: float
    size: RentSize
    status: RentStatus
    createdAt: datetime = Field(default_factory=datetime.now)
    droppedOffAt: Optional[datetime] = None
    pickedUpAt: Optional[datetime] = None