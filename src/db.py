"""
データベースから戦績データを読み書きする。
"""
from typing import Optional
import datetime as dt
import pandas as pd
import sqlalchemy as sa
import src.definitions as d


connection_config = {
    "user": "postgres",
    "password": "",
    "host": "db",
    "port": "5432",
    "database": "postgres",
}
engine = sa.create_engine(
    "postgresql://{user}:{password}@{host}:{port}/{database}".format(
        **connection_config
    )
)


def execute_sql(sql: str) -> list:
    return engine.execute(sa.text(sql))


def save_battles(battles: pd.DataFrame):
    battles.to_sql("battles", con=engine, if_exists="append", index=False)


def load_battles(
    lobby: Optional[d.Lobby] = d.Lobby.XMATCH,
    mode: Optional[d.Mode] = None,
    date_from: Optional[dt.date] = None,
    date_to: Optional[dt.date] = None,
) -> pd.DataFrame:
    sql = "select * from battles"
    options = [
        {"use": lobby is not None, "sql": f"lobby = '{lobby and lobby.value}'"},
        {"use": mode is not None, "sql": f"mode = '{mode and mode.value}'"},
        {"use": date_from is not None, "sql": f"date >= '{date_from}'"},
        {"use": date_to is not None, "sql": f"date <= '{date_to}'"},
    ]
    options = list(filter(lambda x: x["use"], options))

    if len(options) > 0:
        sqls = list(map(lambda x: x["sql"], options))
        sql += " where " + " and ".join(sqls)
    return pd.read_sql(sql=sql, con=engine)
