import re
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
import pandas as pd
import packages.master as m
import packages.definitions as d


def get_ax_ticklabels(ax: Axes):
    """
    グラフの軸ラベルを返す。
    """
    xticklabels = [x.get_text() for x in ax.xaxis.get_ticklabels()]
    yticklabels = [x.get_text() for x in ax.yaxis.get_ticklabels()]
    return xticklabels, yticklabels


def get_ax_size(ax: Axes, fig: Figure):
    """
    グラフのサイズを返す。
    """
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height


def credit(ax: Axes, fig: Figure, text: str, yratio: float = 1.0):
    """
    グラフにクレジット表記を追加する
    """
    width, height = get_ax_size(ax, fig)
    x, y = 1, -36 / height * yratio
    ax.text(
        x=x,
        y=y,
        s=f"{text}\n{d.CREDIT}",
        ha="right",
        va="top",
        fontsize=10,
        transform=ax.transAxes,
    )


def to_players(
    battles: pd.DataFrame,
    exclude_A1: bool = True,
) -> pd.DataFrame:
    """
    戦績データをプレイヤー単位のデータに変換する
    """
    team_cols = [x for x in battles.columns if re.compile("^(alpha|bravo)-.+").match(x)]
    player_cols = [x for x in battles.columns if re.compile("^[AB]\d-.+").match(x)]
    player_names = [
        x[:2] for x in player_cols if re.compile("^[AB]\d-weapon$").match(x)
    ]
    if exclude_A1:
        player_names = [x for x in player_names if x != "A1"]

    def player_name_to_df(player_name: str) -> pd.DataFrame:
        team = "alpha" if player_name[0] == "A" else "bravo"
        exclude_team_cols = [x for x in team_cols if not team in x]
        exclude_player_cols = [x for x in player_cols if x[:2] != player_name]

        exclude_cols = exclude_team_cols + exclude_player_cols
        df = battles.drop(columns=exclude_cols)

        df = df.rename(columns=lambda x: re.sub("^[AB]\d-", "", x))
        df = df.rename(columns=lambda x: re.sub("^(alpha|bravo)", "team", x))
        df["player"] = player_name
        df["team"] = team
        return df

    dfs = [player_name_to_df(x) for x in player_names]
    df = pd.concat(dfs, ignore_index=True)

    # win カラムをプレイヤーが勝利したか否かを示す bool とする
    df["win"] = df["win"] == df["team"]

    # サブ、スペシャル、ブキ種のカラムを追加する
    main_master = m.load_master(m.Master.MAIN_WEAPON)
    df["sub-weapon"] = df["weapon"].map(lambda x: main_master.at[x, "sub-key"])
    df["special-weapon"] = df["weapon"].map(lambda x: main_master.at[x, "special-key"])
    df["weapon-type"] = df["weapon"].map(lambda x: main_master.at[x, "type-key"])

    # 1分辺りのリザルトのカラムを追加する
    base_result_cols = ["kill-assist", "kill", "assist", "death", "special", "inked"]
    for col in base_result_cols:
        df[f"{col}-m"] = df[col] / df["time"] * 60

    # 不要なカラムを削除する
    medal_cols = [x for x in battles.columns if re.compile("^medal\d-.+").match(x)]
    df = df.drop(columns=medal_cols)

    return df


def to_teams(battles: pd.DataFrame) -> pd.DataFrame:
    """
    戦績データをチーム単位のデータに変換する
    """
    team_cols = [x for x in battles.columns if re.compile("^(alpha|bravo)-.+").match(x)]
    player_cols = [x for x in battles.columns if re.compile("^[AB]\d-.+").match(x)]
    team_names = [
        x[:5] for x in team_cols if re.compile("^(alpha|bravo)-inked").match(x)
    ]

    def team_name_to_df(team_name: str) -> pd.DataFrame:
        exclude_team_cols = [x for x in team_cols if not team_name in x]
        exclude_player_cols = [x for x in player_cols if x[:1] != team_name[0].upper()]

        exclude_cols = exclude_team_cols + exclude_player_cols
        df = battles.drop(columns=exclude_cols)

        df = df.rename(columns=lambda x: re.sub("^[AB]", "P", x))
        df = df.rename(columns=lambda x: re.sub("^(alpha|bravo)", "team", x))
        df["team"] = team_name
        return df

    dfs = [team_name_to_df(x) for x in team_names]
    df = pd.concat(dfs, ignore_index=True)

    # win カラムをチームが勝利したか否かを示す bool とする
    df["win"] = df["win"] == df["team"]

    # 不要なカラムを削除する
    medal_cols = [x for x in battles.columns if re.compile("^medal\d-.+").match(x)]
    df = df.drop(columns=medal_cols)

    return df
