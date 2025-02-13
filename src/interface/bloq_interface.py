import abc
from typing import List, Optional

from entity.bloq import Bloq


class BloqRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def get_all(self) -> List[Bloq]:
        pass

    @abc.abstractmethod
    def get_by_id(self, bloq_id: str) -> Optional[Bloq]:
        pass

    @abc.abstractmethod
    def create(self, bloq: Bloq) -> Bloq:
        pass