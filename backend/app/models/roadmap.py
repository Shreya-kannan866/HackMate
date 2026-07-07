"""
Roadmap models — Track C (Person C).

Roadmap:            a curated learning path (e.g. "Full-Stack in 30 Days")
UserRoadmapProgress: tracks how far a given user has gotten through one
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func

from app.database.base import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # Simple JSON list of steps for now, e.g.
    # [{"title": "Learn Git basics", "resource_url": "..."}]
    # Can be split into a proper `roadmap_steps` table later if needed.
    steps = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserRoadmapProgress(Base):
    __tablename__ = "user_roadmap_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # FK -> users.id once Track A's table exists
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False, index=True)
    completed_steps = Column(JSON, nullable=False, default=list)  # list of step indices completed
    status = Column(String, default="not_started")  # not_started | in_progress | completed
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
