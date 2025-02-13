from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from entity.bloq import Bloq
from exceptions.bloq_exceptions import BloqNofFound, BloqError
from persistence.repository.bloq_repository import BloqRepository
from router.dependencies import get_db
from usecase.bloq_usecase import BloqUseCase

router = APIRouter()

@router.get("/", response_model=List[Bloq])
def list_bloqs(db: Session = Depends(get_db)):
    repo = BloqRepository(db)
    usecase = BloqUseCase(repo)
    return usecase.list_bloqs()

@router.get("/{bloq_id}", response_model=Bloq)
def get_bloq(bloq_id: str, db: Session = Depends(get_db)):
    repo = BloqRepository(db)
    usecase = BloqUseCase(repo)
    try:
        return usecase.get_bloq(bloq_id)
    except BloqNofFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=Bloq)
def create_bloq(bloq: Bloq, db: Session = Depends(get_db)):
    repo = BloqRepository(db)
    usecase = BloqUseCase(repo)
    try:
        return usecase.create_bloq(bloq)
    except BloqError as e:
        raise HTTPException(status_code=400, detail=str(e))