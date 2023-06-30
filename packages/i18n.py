import re
import datetime as dt
from string import Template
from enum import Enum
from typing import Optional
import pandas as pd
from packages.master import Master, load_master


class Locale(Enum):
    JA = "ja"
    EN = "en"

def _create_dictionary():
    masters = [
        Master.MAIN_WEAPON,
        Master.SUB_WEAPON,
        Master.SPECIAL_WEAPON,
        Master.RULE,
        Master.STAGE,
        Master.LOBBY,
        Master.ABILITY,
    ]
    dfs = [load_master(x).reset_index()[["key", "name-ja", "name-en"]] for x in masters]
    df = pd.concat(dfs, ignore_index=True).rename(columns=lambda x: re.sub("^name-", "", x)).set_index("key")
    dictionary = df.to_dict(orient="index")
    return dictionary


class Translator:
    def __init__(self, locale: Optional[Locale] = Locale.JA):
        self.set_locale(locale)
        self._dictionary = _create_dictionary()
        self.add("mean", "平均値", "Avg.")
        self.add("New Season Challenge", "新シーズン開幕記念カップ", "New Season Challenge")
        self.add("Too Many Trizookas!", "ウルトラショット祭り", "Too Many Trizookas")
        self.add("The Sheldon Sampler Challenge", "いろんなブキをかわいがるブキチ杯", "The Sheldon Sampler Challenge")
        self.add("Monthly Challenge", "ツキイチ・イベントマッチ", "Monthly Challenge")
        self.add("Foggy Notion", "霧の中の戦い", "Foggy Notion")

    def set_locale(self, locale: Locale):
        self.locale = locale

    def t(self, key: str, **kwargs) -> str:
        locale = kwargs.pop("locale", self.locale)
        translation = self._dictionary[key][locale.value]
        return Template(translation).substitute(**kwargs)

    def add(self, key: str, label_ja: str, label_en: str):
        self._dictionary |= { key: { "ja": label_ja, "en": label_en } }

    def t_date(self, date: dt.date, locale: Optional[Locale] = None) -> str:
        locale = locale or self.locale
        match locale:
            case Locale.JA:
                format = "%-m/%-d"
            case Locale.EN:
                format = "%b. %-d"
            case _:
                format = "%-m/%-d"
        return date.strftime(format)

    def t_duration(self, date_from: dt.date, date_to: dt.date, locale: Optional[Locale] = None) -> str:
        locale = locale or self.locale
        d1 = self.t_date(date_from, locale=locale)
        d2 = self.t_date(date_to, locale=locale)
        match locale:
            case Locale.JA:
                return f"{d1}〜{d2}"
            case Locale.EN:
                return f"{d1} - {d2}"
            case _:
                return f"{d1}〜{d2}"

    def t_data_duration(self, data: pd.DataFrame, locale: Optional[Locale] = None) -> str:
        locale = locale or self.locale
        date_from = data["date"].min()
        date_to = data["date"].max()
        return self.t_duration(date_from, date_to, locale=locale)
