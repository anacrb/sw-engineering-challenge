from enum import Enum

from pydantic import BaseModel


class LockerStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Locker(BaseModel):
    id: str
    bloqId: str
    status: LockerStatus
    isOccupied: bool