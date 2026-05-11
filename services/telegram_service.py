import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

def enviarMensaje(chat_id, texto, parse_mode=None):
    payload = {
        "chat_id": chat_id,
        "text": texto
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)