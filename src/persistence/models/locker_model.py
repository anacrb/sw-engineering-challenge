from sqlalchemy import Column, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship

from entity.locker import LockerStatus
from persistence.postgres_config import Base


class LockerModel(Base):
    __tablename__ = "lockers"

    id = Column(String, primary_key=True, index=True)
    bloqId = Column(String, ForeignKey("bloqs.id"), nullable=False)
    status = Column(Enum(LockerStatus), nullable=False)
    isOccupied = Column(Boolean, default=False, nullable=False)

    # Relationship back to Bloq
    bloq = relationship("BloqModel", back_populates="lockers")

    # Relationship to Rents
    rents = relationship("RentModel", back_populates="locker")