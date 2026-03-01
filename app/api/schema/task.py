from sqlmodel import SQLModel
from datetime import datetime
from app.database.model.task import TaskProgress


class BaseTask(SQLModel):
    title: str
    status: TaskProgress


class ReadTask(BaseTask):
    created_at: datetime


class CreateTask(BaseTask):
    pass
