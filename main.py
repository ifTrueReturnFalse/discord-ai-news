import os
from dotenv import load_dotenv
from discord import send_embed, DiscordPayload
from ai_api.gemini import ask_gemini
import time

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

if __name__ == "__main__":
    persona = "Tu es un journaliste jeux vidéos. Ton objectif est de trouver des articles de la semaine."
    query = f"Nous sommes le {time.time()}. Fais un résumer de maximum 10 news importantes. Chaque article doit avoir son embed comme fourni."
    results = ask_gemini(query, persona, language='francais')

    data: DiscordPayload = {
        "embeds": results
    }

    send_embed(DISCORD_WEBHOOK_URL, data)

