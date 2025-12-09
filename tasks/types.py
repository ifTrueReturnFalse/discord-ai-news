from pydantic import BaseModel
from typing import List

# Task model expected in the config file
class Task(BaseModel):
    title: str
    persona: str
    query: str
    language: str
    discord_webhook: str

# The config file is a list of 'Task'
class TasksConfig(BaseModel):
    tasks: List[Task]