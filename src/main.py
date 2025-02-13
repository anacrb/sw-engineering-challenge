import uvicorn
from fastapi import FastAPI

from persistence.postgres_config import Base, engine
from router.bloq_router import router as bloq


def create_app() -> FastAPI:
    # Create tables if not present (demo only; use Alembic in production)
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Bloqit with Use Cases & Postgres")

    app.include_router(bloq, prefix="/bloqs", tags=["Bloqs"])

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)