"""
マスターデータを管理する。
"""
import os
import re
import json
from enum import Enum
import requests
import pandas as pd
from bs4 import BeautifulSoup
import packages.definitions as d


def update_weapon_master():
    """
    メインウェポン、サブウェポン、スペシャルウェポン、ブキタイプのマスターデータを取得し、csv ファイルとして格納する。
    """
    os.makedirs(d.MASTERS_DIR, exist_ok=True)
    r = requests.get(d.STATINK_API_WEAPON_URL)
    weapon_json = json.loads(r.content)

    def to_weapon_obj(data: object) -> object:
        return {
            "key": data["key"],
            "name-ja": data["name"]["ja_JP"],
            "name-en": data["name"]["en_US"],
            "type-key": data["type"]["key"],
            "type-name-ja": data["type"]["name"]["ja_JP"],
            "type-name-en": data["type"]["name"]["en_US"],
            "sub-key": data["sub"]["key"],
            "sub-name-ja": data["sub"]["name"]["ja_JP"],
            "sub-name-en": data["sub"]["name"]["en_US"],
            "special-key": data["special"]["key"],
            "special-name-ja": data["special"]["name"]["ja_JP"],
            "special-name-en": data["special"]["name"]["en_US"],
        }

    main_weapon = pd.DataFrame(list(map(to_weapon_obj, weapon_json)))
    main_weapon.to_csv(d.MASTER_MAIN_WEAPON_PATH, index=False)

    sub_weapon = (
        main_weapon[["sub-key", "sub-name-ja", "sub-name-en"]]
        .rename(columns=lambda x: re.sub("^sub-", "", x))
        .drop_duplicates()
    )
    sub_weapon.to_csv(d.MASTER_SUB_WEAPON_PATH, index=False)

    special_weapon = (
        main_weapon[["special-key", "special-name-ja", "special-name-en"]]
        .rename(columns=lambda x: re.sub("^special-", "", x))
        .drop_duplicates()
    )
    special_weapon.to_csv(d.MASTER_SPECIAL_WEAPON_PATH, index=False)

    weapon_type = (
        main_weapon[["type-key", "type-name-ja", "type-name-en"]]
        .rename(columns=lambda x: re.sub("^type-", "", x))
        .drop_duplicates()
    )
    weapon_type.to_csv(d.MASTER_WEAPON_TYPE_PATH, index=False)


def update_weapon_pool_master():
    r = requests.get(d.STATINK_API_WEAPON_INFO_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table")
    header_texts = [x.text for x in table.select("thead th")]

    pool_th_index = header_texts.index("X")
    key_th_index = header_texts.index("key")

    trs = table.select("tbody tr")

    def get_weapon_pool(tr) -> tuple[str, str]:
        tds = tr.find_all("td", recursive=False)
        pool = tds[pool_th_index].get("title").lower().replace(" ", "")
        key = tds[key_th_index].text
        return { "key": key, "pool": pool }

    weapon_pool = pd.DataFrame([get_weapon_pool(x) for x in trs])
    weapon_pool.to_csv(d.MASTER_WEAPON_POOL_PATH, index=False)


def update_rule_master():
    """
    ルールのマスターデータを取得し、csv ファイルとして格納する。
    """
    os.makedirs(d.MASTERS_DIR, exist_ok=True)
    r = requests.get(d.STATINK_API_RULE_URL)
    rule_json = json.loads(r.content)

    def to_rule_obj(data: object) -> object:
        return {
            "key": data["key"],
            "name-ja": data["short_name"]["ja_JP"],
            "name-en": data["short_name"]["en_US"],
        }

    rule = pd.DataFrame(list(map(to_rule_obj, rule_json)))
    rule.to_csv(d.MASTER_RULE_PATH, index=False)


def update_stage_master():
    """
    ステージのマスターデータを取得し、csv ファイルとして格納する。
    """
    os.makedirs(d.MASTERS_DIR, exist_ok=True)
    r = requests.get(d.STATINK_API_STAGE_URL)
    stage_json = json.loads(r.content)

    def to_stage_obj(data: object) -> object:
        return {
            "key": data["key"],
            "name-ja": data["name"]["ja_JP"],
            "name-en": data["name"]["en_US"],
        }

    stage = pd.DataFrame(list(map(to_stage_obj, stage_json)))
    stage.to_csv(d.MASTER_STAGE_PATH, index=False)


def update_lobby_master():
    """
    ロビーのマスターデータを取得し、csv ファイルとして格納する。
    """
    os.makedirs(d.MASTERS_DIR, exist_ok=True)
    r = requests.get(d.STATINK_API_LOBBY_URL)
    lobby_json = json.loads(r.content)

    def to_lobby_obj(data: object) -> object:
        return {
            "key": data["key"],
            "name-ja": data["name"]["ja_JP"],
            "name-en": data["name"]["en_US"],
        }

    lobby = pd.DataFrame(list(map(to_lobby_obj, lobby_json)))
    lobby.to_csv(d.MASTER_LOBBY_PATH, index=False)


def update_masters():
    """
    すべてのマスターデータを取得する。
    """
    update_weapon_master()
    update_weapon_pool_master()
    update_rule_master()
    update_stage_master()
    update_lobby_master()


class Master(Enum):
    MAIN_WEAPON = "main_weapon"
    SUB_WEAPON = "sub_weapon"
    SPECIAL_WEAPON = "special_weapon"
    WEAPON_TYPE = "weapon_type"
    WEAPON_POOL = "weapon_pool"
    RULE = "rule"
    STAGE = "stage"
    LOBBY = "lobby"


def load_master(target: Master) -> pd.DataFrame:
    """
    指定したマスターデータの DataFrame を返す。
    """
    match target:
        case Master.MAIN_WEAPON:
            return pd.read_csv(d.MASTER_MAIN_WEAPON_PATH, index_col="key")
        case Master.SUB_WEAPON:
            return pd.read_csv(d.MASTER_SUB_WEAPON_PATH, index_col="key")
        case Master.SPECIAL_WEAPON:
            return pd.read_csv(d.MASTER_SPECIAL_WEAPON_PATH, index_col="key")
        case Master.WEAPON_TYPE:
            return pd.read_csv(d.MASTER_WEAPON_TYPE_PATH, index_col="key")
        case Master.WEAPON_POOL:
            return pd.read_csv(d.MASTER_WEAPON_POOL_PATH, index_col="key")
        case Master.RULE:
            return pd.read_csv(d.MASTER_RULE_PATH, index_col="key")
        case Master.STAGE:
            return pd.read_csv(d.MASTER_STAGE_PATH, index_col="key")
        case Master.LOBBY:
            return pd.read_csv(d.MASTER_LOBBY_PATH, index_col="key")
        case _:
            raise ValueError("target not found")
