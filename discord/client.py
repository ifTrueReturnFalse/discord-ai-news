import requests
from .types import DiscordPayload
from pydantic import TypeAdapter

def send_embed(webhook_url: str | None, payload: DiscordPayload):
    if not webhook_url:
        print("❓ No WebHook URL provided !")
        return

    adapter = TypeAdapter(DiscordPayload)
    payload_clean = adapter.dump_python(payload, mode='json')

    try:
        response = requests.post(
            url=webhook_url,
            json=payload_clean,
            timeout=5
        )

        response.raise_for_status()
        print("📨 Message sent to Discord !")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error while sending to Webhook : {e}")