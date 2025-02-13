from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import relationship

from entity.rent import RentSize, RentStatus
from persistence.postgres_config import Base


class RentModel(Base):
    __tablename__ = "rents"

    id = Column(String, primary_key=True, index=True)
    lockerId = Column(String, ForeignKey("lockers.id"), nullable=False)
    weight = Column(Float, nullable=False)
    size = Column(Enum(RentSize), nullable=False)
    status = Column(Enum(RentStatus), nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    droppedOffAt = Column(DateTime, nullable=True)
    pickedUpAt = Column(DateTime, nullable=True)

    # Relationship back to Locker
    locker = relationship("LockerModel", back_populates="rents")