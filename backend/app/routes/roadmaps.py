"""
HTTP layer for Roadmaps. Thin — just request/response shape and
status codes. All logic lives in services/roadmap_service.py.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import get_current_user, CurrentUser
from app.schemas.roadmap import RoadmapCreate, RoadmapResponse, ProgressUpdate, ProgressResponse
from app.services import roadmap_service

router = APIRouter(prefix="/roadmaps", tags=["roadmaps"])


@router.get("/", response_model=list[RoadmapResponse])
def list_roadmaps(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return roadmap_service.get_all_roadmaps(db, skip, limit)


@router.get("/{roadmap_id}", response_model=RoadmapResponse)
def get_roadmap(roadmap_id: int, db: Session = Depends(get_db)):
    try:
        return roadmap_service.get_roadmap_or_404(db, roadmap_id)
    except roadmap_service.RoadmapNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=RoadmapResponse, status_code=201)
def create_roadmap(payload: RoadmapCreate, db: Session = Depends(get_db)):
    return roadmap_service.create_new_roadmap(db, payload)


@router.post("/{roadmap_id}/progress", response_model=ProgressResponse)
def update_progress(
    roadmap_id: int,
    payload: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    try:
        return roadmap_service.mark_step_complete(
            db, current_user["id"], roadmap_id, payload.completed_step_index
        )
    except roadmap_service.RoadmapNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
