
from pywebpush import webpush, WebPushException
import json, os

VAPID_PRIV = os.getenv("VAPID_PRIVATE_KEY")
VAPID_CLAIMS = {"sub": "mailto:admin@example.com"}

def send_push(subscription_json: str, data: dict):
    sub = json.loads(subscription_json)
    try:
        webpush(
            subscription_info=sub,
            data=json.dumps(data),
            vapid_private_key=VAPID_PRIV,
            vapid_claims=VAPID_CLAIMS,
        )
    except WebPushException as exc:
        print("Push error", exc)
