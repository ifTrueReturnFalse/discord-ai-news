import requests
from .types import DiscordPayload
from pydantic import TypeAdapter

# Function to send a message, with or without embeds
def send_embed(webhook_url: str | None, payload: DiscordPayload):
    print("Sending a message to Discord")
    # Stop if no webhook is provided
    if not webhook_url:
        print("❓ No WebHook URL provided !")
        return

    adapter = TypeAdapter(DiscordPayload)
    payload_clean = adapter.dump_python(payload, mode="json")

    try:
        # Send the payload to the webhook
        response = requests.post(url=webhook_url, json=payload_clean, timeout=5)
        # Raise an error if their is a problem
        response.raise_for_status()
        print("📨 Message sent to Discord !")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error while sending to Webhook : {e}")
