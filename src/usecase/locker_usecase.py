from typing import List

from entity.locker import Locker
from exceptions.locker_exceptions import LockerNotFound, FailedToUpdateLocker
from interface.locker_interface import LockerRepositoryInterface


class LockerUseCase:
    """
    Business logic for Lockers, e.g. updating status or isOccupied, etc.
    """

    def __init__(self, locker_repo: LockerRepositoryInterface):
        self.locker_repo = locker_repo

    def create_locker(self, locker: Locker) -> Locker:
        return self.locker_repo.create(locker)

    def list_lockers(self) -> List[Locker]:
        return self.locker_repo.get_all()

    def get_locker(self, locker_id: str) -> Locker:
        l = self.locker_repo.get_by_id(locker_id)
        if not l:
            raise LockerNotFound(locker_id)
        return l

    def update_locker(self, locker_id: str, new_data: Locker) -> Locker:
        existing = self.locker_repo.get_by_id(locker_id)
        if not existing:
            raise LockerNotFound(locker_id)
        updated = self.locker_repo.update(locker_id, new_data)
        if not updated:
            raise FailedToUpdateLocker
        return updated
