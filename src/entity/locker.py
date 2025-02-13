from enum import Enum

from pydantic import BaseModel, ConfigDict


class LockerStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Locker(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    bloqId: str
    status: LockerStatus
    isOccupied: bool