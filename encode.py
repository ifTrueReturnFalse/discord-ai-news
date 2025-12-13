import base64
import os

tasks_file_path: str = "tasks.json"

if os.path.exists(tasks_file_path):
    try:
        with open(tasks_file_path, "rb") as file:
            print("Copy this string in your TASKS_JSON environnement variable : ")
            print('-' * 40)
            print(base64.b64encode(file.read()).decode('utf-8'))
            print('-' * 40)
    except Exception as e:
        print(f"Oops, something went wrong while encoding to base 64 : {e}")