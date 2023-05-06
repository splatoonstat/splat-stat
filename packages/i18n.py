import datetime as dt
from enum import Enum
from typing import Optional
import pandas as pd
import packages.definitions as d


class Locale(Enum):
    JA = "ja"
    EN = "en"


def get_translations(
    custom_translation_df: Optional[pd.DataFrame] = None, locale: Locale = Locale.JA
) -> pd.DataFrame:
    """
    翻訳用の辞書を返却する。
    custom_translation_df はカスタム翻訳用の DataFrame オブジェクト。
    custom_translation_df は `key`, `name-ja`, `name-en` のカラムを持つ必要がある。
    """
    masters = [
        d.MASTER_MAIN_WEAPON_PATH,
        d.MASTER_SUB_WEAPON_PATH,
        d.MASTER_SPECIAL_WEAPON_PATH,
        d.MASTER_RULE_PATH,
        d.MASTER_STAGE_PATH,
        d.MASTER_LOBBY_PATH,
    ]
    dfs = list(map(lambda x: pd.read_csv(x)[["key", "name-ja", "name-en"]], masters))
    dfs = dfs + [
        pd.DataFrame(
            [
                {"key": "mean", "name-ja": "平均値", "name-en": "Ave."},
                {"key": "median", "name-ja": "中央値", "name-en": "Median"},
            ]
        )
    ]
    if custom_translation_df is not None:
        dfs = dfs + [custom_translation_df]

    df = pd.concat(dfs, ignore_index=True).set_index("key")

    name_key = f"name-{locale.value}"
    return df[name_key].to_dict()


def date_to_str(date: dt.date, locale: Locale = Locale.JA) -> str:
    """
    date オブジェクトを locale に合った文字列に変換し返却する。
    """
    match locale:
        case Locale.JA:
            format = "%-m/%-d"
        case Locale.EN:
            format = "%b. %-d"
        case _:
            format = "%-m/%-d"
    return date.strftime(format)


def duration_to_str(
    date_from: dt.date, date_to: dt.date, locale: Locale = Locale.JA
) -> str:
    d1 = date_to_str(date_from, locale=locale)
    d2 = date_to_str(date_to, locale=locale)
    match locale:
        case Locale.JA:
            return f"{d1}〜{d2}"
        case Locale.EN:
            return f"{d1} - {d2}"
        case _:
            return f"{d1}〜{d2}"


def battles_to_duration_str(battles: pd.DataFrame, locale: Locale = Locale.JA) -> str:
    """
    battles の開催期間を locale に合った文字列に変換し返却する。
    """
    date_from = battles["date"].min()
    date_to = battles["date"].max()
    return duration_to_str(date_from, date_to, locale=locale)
