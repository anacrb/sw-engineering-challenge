from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from entity.rent import Rent
from exceptions.locker_exceptions import LockerNotFound
from exceptions.rent_exceptions import RentError, InvalidStatus, RentNotFound, RentNotFoundDuringUpdate
from persistence.repository.locker_repository import LockerRepository
from persistence.repository.rent_repository import RentRepository
from router.dependencies import get_db
from usecase.rent_usecase import RentUseCase

router = APIRouter()

@router.get("/", response_model=List[Rent])
def list_rents(db: Session = Depends(get_db)):
    rent_repo = RentRepository(db)
    locker_repo = LockerRepository(db)
    usecase = RentUseCase(rent_repo, locker_repo)
    return usecase.list_rents()

@router.get("/{rent_id}", response_model=Rent)
def get_rent(rent_id: str, db: Session = Depends(get_db)):
    rent_repo = RentRepository(db)
    locker_repo = LockerRepository(db)
    usecase = RentUseCase(rent_repo, locker_repo)
    try:
        return usecase.get_rent(rent_id)
    except RentNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=Rent)
def create_rent(rent: Rent, db: Session = Depends(get_db)):
    rent_repo = RentRepository(db)
    locker_repo = LockerRepository(db)
    usecase = RentUseCase(rent_repo, locker_repo)
    try:
        return usecase.create_rent(rent)
    except RentError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{rent_id}/dropoff", response_model=Rent)
def dropoff_parcel(rent_id: str, db: Session = Depends(get_db)):
    rent_repo = RentRepository(db)
    locker_repo = LockerRepository(db)
    usecase = RentUseCase(rent_repo, locker_repo)
    try:
        return usecase.dropoff_parcel(rent_id)
    except InvalidStatus as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (
            RentNotFound,
            RentNotFoundDuringUpdate,
            LockerNotFound
    ) as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{rent_id}/pickup", response_model=Rent)
def pickup_parcel(rent_id: str, db: Session = Depends(get_db)):
    rent_repo = RentRepository(db)
    locker_repo = LockerRepository(db)
    usecase = RentUseCase(rent_repo, locker_repo)
    try:
        return usecase.pickup_parcel(rent_id)
    except InvalidStatus as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (
            RentNotFound,
            RentNotFoundDuringUpdate,
            LockerNotFound
    ) as e:
        raise HTTPException(status_code=404, detail=str(e))