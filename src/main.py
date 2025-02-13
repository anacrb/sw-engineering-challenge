import uvicorn
from fastapi import FastAPI

from persistence.postgres_config import Base, engine
from router.bloq_router import router as bloq
from router.locker_router import router as locker
from router.rent_router import router as rent


def create_app() -> FastAPI:
    # Create tables if not present (demo only; use Alembic in production)
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Bloqit with Use Cases & Postgres")

    app.include_router(bloq, prefix="/bloqs", tags=["Bloqs"])
    app.include_router(locker, prefix="/lockers", tags=["Lockers"])
    app.include_router(rent, prefix="/rents", tags=["Rents"])

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)