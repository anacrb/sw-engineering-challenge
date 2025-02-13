from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from persistence.postgres_config import Base


class BloqModel(Base):
    __tablename__ = "bloqs"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # Relationship to Lockers
    lockers = relationship("LockerModel", back_populates="bloq")