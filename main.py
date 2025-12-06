import os
from dotenv import load_dotenv
from discord import send_embed, DiscordEmbed, DiscordPayload

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

if __name__ == "__main__":
    embed: DiscordEmbed = {
        "title": "Un petit titre cliquable !",
        "url": "https://youtube.com",
        "description": "Pleins de blabla",
        "color": 0xfc3503,
        "fields": [
            {"name": "Un truc", "value": "Une valeur"}
        ]
    }

    data: DiscordPayload = {
        "embeds": [embed]
    }

    send_embed(DISCORD_WEBHOOK_URL, data)

