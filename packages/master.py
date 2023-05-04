"""
マスターデータを管理する。
"""
import os
import re
import json
from enum import Enum
import requests
import pandas as pd
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
    update_rule_master()
    update_stage_master()
    update_lobby_master()


def load_master(target: d.Master) -> pd.DataFrame:
    """
    指定したマスターデータの DataFrame を返す。
    """
    match target:
        case d.Master.MAIN_WEAPON:
            return pd.read_csv(d.MASTER_MAIN_WEAPON_PATH)
        case d.Master.SUB_WEAPON:
            return pd.read_csv(d.MASTER_SUB_WEAPON_PATH)
        case d.Master.SPECIAL_WEAPON:
            return pd.read_csv(d.MASTER_SPECIAL_WEAPON_PATH)
        case d.Master.WEAPON_TYPE:
            return pd.read_csv(d.MASTER_WEAPON_TYPE_PATH)
        case d.Master.RULE:
            return pd.read_csv(d.MASTER_RULE_PATH)
        case d.Master.STAGE:
            return pd.read_csv(d.MASTER_STAGE_PATH)
        case d.Master.LOBBY:
            return pd.read_csv(d.MASTER_LOBBY_PATH)
        case _:
            raise ValueError("target not found")
