"""
Raw DB query logic for Roadmaps — no business rules here, that
belongs in services/roadmap_service.py.
"""
from sqlalchemy.orm import Session

from app.models.roadmap import Roadmap, UserRoadmapProgress


def list_roadmaps(db: Session, skip: int = 0, limit: int = 20) -> list[Roadmap]:
    return db.query(Roadmap).offset(skip).limit(limit).all()


def get_roadmap(db: Session, roadmap_id: int) -> Roadmap | None:
    return db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()


def create_roadmap(db: Session, title: str, description: str | None, steps: list[dict]) -> Roadmap:
    roadmap = Roadmap(title=title, description=description, steps=steps)
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)
    return roadmap


def get_progress(db: Session, user_id: int, roadmap_id: int) -> UserRoadmapProgress | None:
    return (
        db.query(UserRoadmapProgress)
        .filter(UserRoadmapProgress.user_id == user_id, UserRoadmapProgress.roadmap_id == roadmap_id)
        .first()
    )


def upsert_progress(db: Session, user_id: int, roadmap_id: int, completed_steps: list[int], status: str) -> UserRoadmapProgress:
    progress = get_progress(db, user_id, roadmap_id)
    if progress is None:
        progress = UserRoadmapProgress(
            user_id=user_id, roadmap_id=roadmap_id, completed_steps=completed_steps, status=status
        )
        db.add(progress)
    else:
        progress.completed_steps = completed_steps
        progress.status = status
    db.commit()
    db.refresh(progress)
    return progress
