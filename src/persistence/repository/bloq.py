from typing import List, Optional

from sqlalchemy.orm import Session

from entity.bloq import Bloq
from exceptions import BloqAlreadyExists, FailedToCreatBloq
from interface.bloq_interface import BloqRepositoryInterface
from persistence.models.bloq_model import BloqModel


class BloqRepository(BloqRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Bloq]:
        bloqs = self.db.query(BloqModel).all()
        return [Bloq.model_validate(bloq) for bloq in bloqs]

    def get_by_id(self, bloq_id: str) -> Optional[Bloq]:
        bloq = self.db.query(BloqModel).filter(BloqModel.id == bloq_id).first()
        if not bloq:
            return None
        return Bloq.model_validate(bloq)

    def create(self, bloq: Bloq) -> Bloq:
        existing = self.db.query(BloqModel).filter(BloqModel.id == bloq.id).first()
        if existing:
            raise BloqAlreadyExists(bloq.id)

        try:
            bloq_model = BloqModel(**bloq.model_dump())
            self.db.add(bloq_model)
            self.db.commit()
            return bloq
        except Exception as e:
            raise FailedToCreatBloq