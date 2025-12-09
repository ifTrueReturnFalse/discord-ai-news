import os
from discord import send_embed
from ai_api.gemini import ask_gemini
import time
import json
from tasks import Task, TasksConfig
from typing import Optional, List
from pydantic import ValidationError

def main() -> None:
    tasks_file_path: str = "tasks.json"
    tasks_config: Optional[TasksConfig] = None

    if os.path.exists(tasks_file_path):
        try:
            with open(tasks_file_path, 'r', encoding='utf-8') as file:
                raw_data: str = file.read()
                tasks_config = TasksConfig.model_validate_json(raw_data)
        except ValidationError as e:
            print(f"Validation error in {tasks_file_path}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error while decoding file: {e}")
        except Exception as e:
            print(f"Something went wrong: {e}")
    else:
        print("Loading secret tasks in env...")

    if not tasks_config:
        print("No correct config file.")
        return

    tasks_list: List[Task] = tasks_config.tasks
    if tasks_list:
        print(f"{len(tasks_list)} to process.")
        for task in tasks_list:
            print(f"Processing '{task.title}'")

            ai_result = ask_gemini(task.query, task.persona, task.language)
            if ai_result is None:
                print("Can't send nothing to Discord")
                continue
            else:
                send_embed(task.discord_webhook, ai_result)
            time.sleep(20)

if __name__ == "__main__":
    main()