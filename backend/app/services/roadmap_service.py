"""
Business logic for Roadmaps — the routes/roadmaps.py file should
never talk to the repository directly, it should always go through here.
"""
from sqlalchemy.orm import Session

from app.repositories import roadmap_repository
from app.schemas.roadmap import RoadmapCreate


class RoadmapNotFoundError(Exception):
    pass


def get_all_roadmaps(db: Session, skip: int = 0, limit: int = 20):
    return roadmap_repository.list_roadmaps(db, skip, limit)


def get_roadmap_or_404(db: Session, roadmap_id: int):
    roadmap = roadmap_repository.get_roadmap(db, roadmap_id)
    if roadmap is None:
        raise RoadmapNotFoundError(f"Roadmap {roadmap_id} not found")
    return roadmap


def create_new_roadmap(db: Session, payload: RoadmapCreate):
    steps_as_dicts = [step.model_dump() for step in payload.steps]
    return roadmap_repository.create_roadmap(db, payload.title, payload.description, steps_as_dicts)


def mark_step_complete(db: Session, user_id: int, roadmap_id: int, step_index: int):
    roadmap = get_roadmap_or_404(db, roadmap_id)

    existing = roadmap_repository.get_progress(db, user_id, roadmap_id)
    completed = set(existing.completed_steps) if existing else set()
    completed.add(step_index)

    total_steps = len(roadmap.steps)
    status = "completed" if len(completed) >= total_steps else "in_progress"

    return roadmap_repository.upsert_progress(
        db, user_id, roadmap_id, sorted(completed), status
    )
