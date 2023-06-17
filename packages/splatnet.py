import json
import requests

def fetch(data: dict, gtoken: str, bullet_token: str) -> dict:
    url = "https://api.lp1.av5ja.srv.nintendo.net/api/graphql"
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"_gtoken: {gtoken}",
        "Authorization": f"Bearer {bullet_token}",
        "X-Web-View-Ver": "2.0.0-7070f95e",
        "Referer": "https://api.lp1.av5ja.srv.nintendo.net/?lang=ja-JP&na_country=JP&na_lang=ja-JP"
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return json.loads(r.content)
