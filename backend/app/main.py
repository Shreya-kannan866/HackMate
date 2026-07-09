"""
App entrypoint. Run locally with:
    uvicorn app.main:app --reload

This is [Shared] scaffolding — as Person A and Person B build their
routes, they each add one line here: `app.include_router(their_router)`.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.base import Base
from app.database.session import engine

# --- Import models so Base.metadata knows about every table ---
# Add your model imports here as each track builds theirs, e.g.:
# from app.models import user, opportunity, team, application, workspace, review, reputation
from app.models import roadmap  # noqa: F401  (Track C)
from app.models import user, reputation, notification

# --- Import routers ---
from app.routes import roadmaps
from app.routes import auth, users, reputation, notifications  # Fixed: Imported from app.routes instead of app.dependencies

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)          # Add this
app.include_router(users.router)         # Add this
app.include_router(reputation.router)    # Add this
app.include_router(notifications.router) # Add this
# Dev-only convenience: auto-creates tables from models on startup.
# Once Alembic migrations are set up (shared task), replace this with
# `alembic upgrade head` run as a separate step instead.
Base.metadata.create_all(bind=engine)

app.include_router(roadmaps.router)
# Person A adds: app.include_router(auth.router)
# Person A adds: app.include_router(users.router)
# Person B adds: app.include_router(opportunities.router)
# Person B adds: app.include_router(teams.router)
# Person C adds later: app.include_router(mock_hackathons.router)
# Person C adds later: app.include_router(workspace.router)


@app.get("/")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}