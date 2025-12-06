import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def send_to_discord(webhook_url: str, content: str) -> None:
    # Security test : stop if no webhook provided
    if not webhook_url:
        print("No webhook to send the message.")
        return

    # Payload format
    data = {
        'content': content
    }

    try: 
        # Sending the message to Discord
        result = requests.post(
            url=webhook_url,
            json=data,
            timeout=10
        )

        # Raise an error if one occured while sending the message
        result.raise_for_status()
        print(f"✅ Message sent ! Code : {result.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error while sending to Discord : ${e}")

if __name__ == "__main__":
    send_to_discord(DISCORD_WEBHOOK_URL, "Coucou ceci est un test !")
