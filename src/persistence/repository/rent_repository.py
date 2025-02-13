from typing import List, Optional

from sqlalchemy.orm import Session

from entity.rent import Rent
from exceptions.rent_exceptions import FailedToCreateRent, RentAlreadyExists
from interface.rent_interface import RentRepositoryInterface
from persistence.models.rent_model import RentModel


class RentRepository(RentRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Rent]:
        rents = self.db.query(RentModel).all()
        return [Rent.model_validate(rent) for rent in rents]

    def get_by_id(self, rent_id: str) -> Optional[Rent]:
        rent = self.db.query(RentModel).filter(RentModel.id == rent_id).first()
        if not rent:
            return None
        return Rent.model_validate(rent)

    def create(self, rent: Rent) -> Rent:
        existing = self.db.query(RentModel).filter(RentModel.id == rent.id).first()
        if existing:
            raise RentAlreadyExists(rent.id)
        try:
            rent_model = RentModel(**rent.dict())
            self.db.add(rent_model)
            self.db.commit()
            return rent
        except Exception as e:
            raise FailedToCreateRent

    def update(self, rent_id: str, new_data: Rent) -> Optional[Rent]:
        rent = self.db.query(RentModel).filter(RentModel.id == rent_id).first()
        if not rent:
            return None
        rent.weight = new_data.weight
        rent.size = new_data.size
        rent.status = new_data.status
        rent.createdAt = new_data.createdAt
        rent.droppedOffAt = new_data.droppedOffAt
        rent.pickedUpAt = new_data.pickedUpAt

        self.db.commit()
        self.db.refresh(rent)
        return Rent.model_validate(rent)
