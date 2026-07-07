"""
Single declarative base shared by every model in the project.
Every file in app/models/ must import Base from here, so that
Base.metadata knows about all tables when migrations/create_all run.
"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()
