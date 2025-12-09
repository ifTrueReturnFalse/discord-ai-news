import os
from discord import send_embed
from ai_api.gemini import ask_gemini
import time
from tasks import Task, TasksConfig
from typing import Optional, List
from pydantic import ValidationError


def main() -> None:
    tasks_file_path: str = "tasks.json"
    tasks_config: Optional[TasksConfig] = None

    # Check if their is a local tasks file
    if os.path.exists(tasks_file_path):
        try:
            with open(tasks_file_path, "r", encoding="utf-8") as file:
                # Raw reading
                raw_data: str = file.read()
                # Validate the config file
                tasks_config = TasksConfig.model_validate_json(raw_data)
        # Validation error
        except ValidationError as e:
            print(f"Validation error in {tasks_file_path}: {e}")
        # Unexpected error
        except Exception as e:
            print(f"Something went wrong: {e}")
    # Not impleted yet
    else:
        print("Loading secret tasks in env...")

    # Exit if no config file found
    if not tasks_config:
        print("No correct config file.")
        return

    # Get tasks
    tasks_list: List[Task] = tasks_config.tasks
    if tasks_list:
        print(f"{len(tasks_list)} to process.")
        # Process all the tasks
        for task in tasks_list:
            print(f"Processing '{task.title}'")
            # Ask Gemini
            ai_result = ask_gemini(task.query, task.persona, task.language)

            if ai_result is None:
                print("Can't send nothing to Discord")
                continue
            else:
                # If I get a result -> send it to Discord
                send_embed(task.discord_webhook, ai_result)
            # Wait to avoid max request per minute (RPM)
            time.sleep(20)


if __name__ == "__main__":
    main()
