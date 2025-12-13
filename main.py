import os
from discord import send_embed
from ai_api.gemini import ask_gemini
import time
from tasks import Task, TasksConfig
from typing import Optional, List
from pydantic import ValidationError
from dotenv import load_dotenv
import base64
import binascii


def main() -> None:
    # Loading environnement
    load_dotenv()
    
    tasks_file_path: str = "tasks.json"
    env_tasks_config = os.getenv('TASKS_JSON')
    tasks_config: Optional[TasksConfig] = None

    # Check the config in the .env file
    if env_tasks_config:
        print("Loading env config")
        try:
            tasks_decoded = base64.b64decode(env_tasks_config).decode('utf-8')
            tasks_config = TasksConfig.model_validate_json(tasks_decoded)
        except binascii.Error as e:
            print(f"Error in the env configuration, Base64 invalid or corrupted : {e}")
            return
        except UnicodeDecodeError as e:
            print(f"Error, decoding done but result is not valid UTF-8 : {e}")
            return
        except ValidationError as e:
            print(f"Environnement tasks config not in the correct format : {e}")
            return
        except Exception as e:
            print(f"Error while loading configuration : {e}")
            return

    # Check if their is a local tasks file
    elif os.path.exists(tasks_file_path):
        print("Loading local config")
        try:
            with open(tasks_file_path, "r", encoding="utf-8") as file:
                # Raw reading
                raw_data: str = file.read()
                # Validate the config file
                tasks_config = TasksConfig.model_validate_json(raw_data)
        # Validation error
        except ValidationError as e:
            print(f"Validation error in {tasks_file_path}: {e}")
            return
        # Unexpected error
        except Exception as e:
            print(f"Something went wrong: {e}")
            return

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
