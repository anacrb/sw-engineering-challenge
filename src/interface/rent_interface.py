import abc
from typing import List, Optional

from entity.rent import Rent


class RentRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def get_all(self) -> List[Rent]:
        pass

    @abc.abstractmethod
    def get_by_id(self, rent_id: str) -> Optional[Rent]:
        pass

    @abc.abstractmethod
    def create(self, rent: Rent) -> Rent:
        pass

    @abc.abstractmethod
    def update(self, rent_id: str, new_data: Rent) -> Optional[Rent]:
        pass