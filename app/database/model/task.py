from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field


class TaskProgress(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class Task(SQLModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    status: TaskProgress = Field(default=TaskProgress.not_started)
    created_at: datetime = Field(default_factory=datetime.now)


tasks = [
    Task(title="Set up project repository", status=TaskProgress.completed),
    Task(title="Design database schema", status=TaskProgress.completed),
    Task(title="Build REST API endpoints", status=TaskProgress.in_progress),
    Task(title="Write unit tests", status=TaskProgress.in_progress),
    Task(title="Deploy to production", status=TaskProgress.not_started),
]
