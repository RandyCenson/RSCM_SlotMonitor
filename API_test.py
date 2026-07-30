import requests

TOKEN = "8920592883:AAHZcl6j4mz23uVYrd1nkgNu-OzGkS0aalc"
CHAT_ID = "5382745861"

r = requests.get(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    params={
        "chat_id": CHAT_ID,
        "text": "test"
    },
    timeout=30
)

print(r.status_code)
print(r.text)