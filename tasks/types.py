from pydantic import BaseModel, HttpUrl
from typing import List

class Task(BaseModel):
    title: str
    persona: str
    query: str
    language: str
    discord_webhook: str

class TasksConfig(BaseModel):
    tasks: List[Task]