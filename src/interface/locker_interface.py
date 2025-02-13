import abc
from typing import List, Optional

from entity.locker import Locker


class LockerRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def get_all(self) -> List[Locker]:
        pass

    @abc.abstractmethod
    def get_by_id(self, locker_id: str) -> Optional[Locker]:
        pass

    @abc.abstractmethod
    def create(self, locker: Locker) -> Locker:
        pass

    @abc.abstractmethod
    def update(self, locker_id: str, updated_data: Locker) -> Optional[Locker]:
        pass