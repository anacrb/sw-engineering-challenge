from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from entity.locker import Locker
from exceptions.locker_exceptions import LockerError, LockerNotFound, FailedToUpdateLocker
from persistence.repository.locker_repository import LockerRepository
from router.dependencies import get_db
from usecase.locker_usecase import LockerUseCase

router = APIRouter()

@router.get("/", response_model=List[Locker])
def list_lockers(db: Session = Depends(get_db)):
    repo = LockerRepository(db)
    usecase = LockerUseCase(repo)
    return usecase.list_lockers()

@router.get("/{locker_id}", response_model=Locker)
def get_locker(locker_id: str, db: Session = Depends(get_db)):
    repo = LockerRepository(db)
    usecase = LockerUseCase(repo)
    try:
        return usecase.get_locker(locker_id)
    except LockerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=Locker)
def create_locker(locker: Locker, db: Session = Depends(get_db)):
    repo = LockerRepository(db)
    usecase = LockerUseCase(repo)
    try:
        return usecase.create_locker(locker)
    except LockerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{locker_id}", response_model=Locker)
def update_locker(locker_id: str, updated_data: Locker, db: Session = Depends(get_db)):
    if updated_data.id != locker_id:
        raise HTTPException(status_code=400, detail="Locker ID mismatch")

    repo = LockerRepository(db)
    usecase = LockerUseCase(repo)
    try:
        return usecase.update_locker(locker_id, updated_data)
    except LockerNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FailedToUpdateLocker as e:
        raise HTTPException(status_code=400, detail=str(e))