"""
データベースから戦績データを読み書きする。
"""
from typing import Optional
import datetime as dt
import pandas as pd
import sqlalchemy as sa
import packages.definitions as d


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
    """
    DB に対して直接 SQL を実行する。
    """
    return engine.execute(sa.text(sql))


def save_battles(battles: pd.DataFrame):
    """
    戦績データを DB に格納する。
    """
    battles.to_sql("battles", con=engine, if_exists="append", index=False)


def load_battles(
    lobby: Optional[d.Lobby] = None,
    mode: Optional[d.Mode] = None,
    date_from: Optional[dt.date] = None,
    date_to: Optional[dt.date] = None,
    replace_heroshooter_to_sshooter: bool = True,
) -> pd.DataFrame:
    """
    DB から戦績データを読み込んで DataFrame として返却する。
    """
    sql = "select * from battles"
    options = [
        {"use": lobby is not None, "sql": f"lobby = '{lobby and lobby.value}'"},
        {"use": mode is not None, "sql": f"mode = '{mode and mode.value}'"},
        {"use": date_from is not None, "sql": f"date >= '{date_from}'"},
        {"use": date_to is not None, "sql": f"date <= '{date_to}'"},
    ]
    options = [x for x in options if x["use"]]

    if len(options) > 0:
        sqls = [x["sql"] for x in options]
        sql += " where " + " and ".join(sqls)
    df = pd.read_sql(sql=sql, con=engine)

    # ヒーローシューターレプリカをスプラシューターに置換する
    if replace_heroshooter_to_sshooter:
        df = df.replace("heroshooter_replica", "sshooter")

    return df
