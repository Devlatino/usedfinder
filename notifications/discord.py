
import os, requests, json

HOOK = os.getenv("DISCORD_WEBHOOK")

def send_discord(item):
    if not HOOK:
        return
    payload = {
        "embeds": [{
            "title": item["title"],
            "url": item["url"],
            "description": f'Prezzo: {item.get("price")} {item.get("currency")}',
        }]
    }
    requests.post(HOOK, json=payload, timeout=10)
