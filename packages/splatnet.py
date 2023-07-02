import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SPLATNET_GTOKEN_ENV = "SPLATNET_GTOKEN"
SPLATNET_BULLET_TOKEN_ENV = "SPLATNET_BULLET_TOKEN"

gtoken = os.environ[SPLATNET_GTOKEN_ENV]
bullet_token = os.environ[SPLATNET_BULLET_TOKEN_ENV]

def fetch(data: dict) -> dict:
    if gtoken == None or bullet_token == None:
        raise Exception(f"Environment variable {SPLATNET_BULLET_TOKEN_ENV} or {SPLATNET_BULLET_TOKEN_ENV} is not set.")

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
