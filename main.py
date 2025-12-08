import os
from dotenv import load_dotenv
from discord import send_embed, DiscordPayload
from ai_api.gemini import ask_gemini
import time
import json

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

if __name__ == "__main__":
    tasks_file_path = "tasks.json"
    tasks_data = {}

    if os.path.exists(tasks_file_path):
        try:
            with open(tasks_file_path, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error while decoding file: {e}")
        except Exception as e:
            print(f"Something went wrong: {e}")
    else:
        print("Loading secret tasks in env...")
    
    tasks_list = tasks_data.get('tasks', [])
    if tasks_list:
        print(f"{len(tasks_list)} to process.")
        for task in tasks_list:
            task_title = task.get('title')
            task_persona = task.get('persona')
            task_query = task.get('query')
            task_language = task.get('language')
            task_discord_webhook = task.get('discord_webhook')

            print(f"Processing '{task_title}'")

            ai_result = ask_gemini(task_query, task_persona, task_language)
            data: DiscordPayload = {
                "embeds": ai_result
            }
            send_embed(task_discord_webhook, data)
            time.sleep(20)

