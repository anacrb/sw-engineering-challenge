from typing import List

from entity.bloq import Bloq
from exceptions.bloq_exceptions import BloqNofFound
from interface.bloq_interface import BloqRepositoryInterface


class BloqUseCase:

    def __init__(self, bloq_repo: BloqRepositoryInterface):
        self.bloq_repo = bloq_repo

    def create_bloq(self, bloq: Bloq) -> Bloq:
        return self.bloq_repo.create(bloq)

    def list_bloqs(self) -> List[Bloq]:
        return self.bloq_repo.get_all()

    def get_bloq(self, bloq_id: str) -> Bloq:
        b = self.bloq_repo.get_by_id(bloq_id)
        if not b:
            raise BloqNofFound(bloq_id)
        return b
