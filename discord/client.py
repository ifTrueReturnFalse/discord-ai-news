import requests
from .types import DiscordPayload

# Function to send a message, with or without embeds
def send_embed(webhook_url: str | None, payload: DiscordPayload):
    print("Sending a message to Discord")
    # Stop if no webhook is provided
    if not webhook_url:
        print("❓ No WebHook URL provided !")
        return

    payload_clean = payload.model_dump(mode='json')

    try:
        # Send the payload to the webhook
        response = requests.post(url=webhook_url, json=payload_clean, timeout=5)
        
        # Debug in case of failure
        if response.status_code == 400:
            print("🚨 DISCORD 400 BAD REQUEST DETECTED")
            print(f"👉 Payload sent (partial): {str(payload_clean)[:500]}...")
            print(f"👉 DISCORD RESPONSE: {response.text}")

        # Raise an error if their is a problem
        response.raise_for_status()
        print("📨 Message sent to Discord !")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error while sending to Webhook : {e}")

        if hasattr(e, 'response') and e.response is not None:
            print(f"🔍 Server Response content: {e.response.text}")
