from typing import List

from sqlalchemy.orm import Session
from typing_extensions import Optional

from entity.locker import Locker
from exceptions.locker_exceptions import FailedToCreateLocker, LockerAlreadyExists
from interface.locker_interface import LockerRepositoryInterface
from persistence.models.locker_model import LockerModel


class LockerRepository(LockerRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Locker]:
        lockers = self.db.query(LockerModel).all()
        return [Locker.model_validate(locker) for locker in lockers]

    def get_by_id(self, locker_id: str) -> Optional[Locker]:
        locker = self.db.query(LockerModel).filter(LockerModel.id == locker_id).first()
        if not locker:
            return None
        return Locker.model_validate(locker)

    def create(self, locker: Locker) -> Locker:
        existing = self.db.query(LockerModel).filter(LockerModel.id == locker.id).first()
        if existing:
            raise LockerAlreadyExists(locker.id)
        try:
            locker_model = LockerModel(**locker.model_dump())
            self.db.add(locker_model)
            self.db.commit()
            return locker
        except Exception as e:
            raise FailedToCreateLocker

    def update(self, locker_id: str, new_data: Locker) -> Optional[Locker]:
        locker = self.db.query(LockerModel).filter(LockerModel.id == locker_id).first()
        if not locker:
            return None
        # Update fields
        locker.bloqId = new_data.bloqId
        locker.status = new_data.status
        locker.isOccupied = new_data.isOccupied

        self.db.commit()
        self.db.refresh(locker)
        return Locker.model_validate(locker)