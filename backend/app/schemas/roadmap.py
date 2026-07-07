"""
Pydantic schemas for the Roadmaps module.
Separate Create/Response/ProgressUpdate schemas — never reuse one
schema for both what a client sends and what the API returns.
"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RoadmapStep(BaseModel):
    title: str
    resource_url: str | None = None


class RoadmapCreate(BaseModel):
    title: str
    description: str | None = None
    steps: list[RoadmapStep] = []


class RoadmapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    steps: list[RoadmapStep]
    created_at: datetime


class ProgressUpdate(BaseModel):
    completed_step_index: int


class ProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    roadmap_id: int
    completed_steps: list[int]
    status: str
    updated_at: datetime
