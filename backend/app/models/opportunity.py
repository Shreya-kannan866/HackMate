
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    opportunity_id = Column(Integer, primary_key=True, index=True)

    created_by = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    hackathon_name = Column(String(150), nullable=False)

    registration_link = Column(String(255), nullable=True)

    deadline = Column(Date, nullable=False)

    domain = Column(String(100), nullable=False)

    description = Column(Text, nullable=False)

    team_size = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    creator = relationship(
        "User",
        back_populates="opportunities"
    )

    teams = relationship(
        "Team",
        back_populates="opportunity",
        cascade="all, delete-orphan"
    )