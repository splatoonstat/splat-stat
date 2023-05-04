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
    if custom_translation_df is not None:
        dfs = dfs + [custom_translation_df]
    df = pd.concat(dfs, ignore_index=True).set_index("key")

    name_key = f"name-{locale.value}"
    return df[name_key].to_dict()
