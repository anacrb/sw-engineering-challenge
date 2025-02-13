from datetime import datetime, timezone
from typing import List

from entity.rent import Rent, RentStatus
from exceptions.locker_exceptions import LockerNotFound
from exceptions.rent_exceptions import RentNotFound, InvalidStatus, RentNotFoundDuringUpdate
from interface.locker_interface import LockerRepositoryInterface
from interface.rent_interface import RentRepositoryInterface


class RentUseCase:

    def __init__(self, rent_repo: RentRepositoryInterface, locker_repo: LockerRepositoryInterface):
        self.rent_repo = rent_repo
        self.locker_repo = locker_repo

    def list_rents(self) -> List[Rent]:
        return self.rent_repo.get_all()

    def get_rent(self, rent_id: str) -> Rent:
        r = self.rent_repo.get_by_id(rent_id)
        if not r:
            raise RentNotFound(rent_id)
        return r

    def create_rent(self, rent: Rent) -> Rent:

        if not rent.createdAt:
            rent.createdAt = datetime.now(timezone.utc)
        if not rent.status:
            rent.status = RentStatus.CREATED

        return self.rent_repo.create(rent)


    def dropoff_parcel(self, rent_id: str) -> Rent:
        rent = self.rent_repo.get_by_id(rent_id)
        if not rent:
            raise RentNotFound(rent_id)

        if rent.status not in (RentStatus.CREATED, RentStatus.WAITING_DROPOFF):
            raise InvalidStatus(rent.status, f"{rent.CREATED} or {RentStatus.WAITING_DROPOFF}")

        # Update rent
        rent.status = RentStatus.WAITING_PICKUP
        rent.droppedOffAt = datetime.now(timezone.utc)
        updated_rent = self.rent_repo.update(rent_id, rent)
        if not updated_rent:
            raise RentNotFoundDuringUpdate

        # Update locker
        locker = self.locker_repo.get_by_id(rent.lockerId)
        if not locker:
            raise LockerNotFound(rent.lockerId)
        locker.isOccupied = True
        self.locker_repo.update(locker.id, locker)

        return updated_rent

    def pickup_parcel(self, rent_id: str) -> Rent:
        rent = self.rent_repo.get_by_id(rent_id)
        if not rent:
            raise RentNotFound(rent_id)

        if rent.status != RentStatus.WAITING_PICKUP:
            raise InvalidStatus(rent.status, RentStatus.WAITING_PICKUP)

        # Update rent
        rent.status = RentStatus.DELIVERED
        rent.pickedUpAt = datetime.now(timezone.utc)
        updated_rent = self.rent_repo.update(rent_id, rent)
        if not updated_rent:
            raise RentNotFoundDuringUpdate(rent_id)

        # Update locker
        locker = self.locker_repo.get_by_id(rent.lockerId)
        if not locker:
            raise LockerNotFound(rent.lockerId)
        locker.isOccupied = False
        self.locker_repo.update(locker.id, locker)

        return updated_rent