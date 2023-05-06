import re
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import packages.master as m
import packages.definitions as d


def get_ax_ticklabels(ax: Axes):
    xticklabels = [x.get_text() for x in ax.xaxis.get_ticklabels()]
    yticklabels = [x.get_text() for x in ax.yaxis.get_ticklabels()]
    return xticklabels, yticklabels


def get_ax_size(ax: Axes, fig: Figure):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height


def credit(ax: Axes, fig: Figure, text: str, yratio: float = 1.0):
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
    additional_columns: list[str] = [],
) -> pd.DataFrame:
    """
    戦績データをプレイヤー単位のデータに変換する
    """
    battle_cols = [
        "season",
        "period",
        "date",
        "game-ver",
        "lobby",
        "mode",
        "stage",
        "time",
        "win",
        "knockout",
        "rank",
        "power",
    ] + additional_columns
    player_cols = [x for x in battles.columns if re.compile("^[AB]\d-.+").match(x)]
    if exclude_A1:
        player_cols = [x for x in player_cols if not re.compile("^A1-.+").match(x)]
    player_names = [
        x[:2] for x in player_cols if re.compile("^[AB]\d-weapon$").match(x)
    ]
    keys = [x[3:] for x in battles.columns if re.compile("^A1-.+").match(x)]

    # 共通データのカラムとプレイヤーデータのカラムに分解する
    df_common = battles[battle_cols].copy()
    df_player = battles[player_cols].copy().fillna("nan")

    # 各プレイヤーの情報を1つのカラムに結合する
    for player_name in player_names:
        df_player[player_name] = (
            df_player[f"{player_name}-{keys[0]}"].astype(str)
            + "/"
            + df_player[f"{player_name}-{keys[1]}"].astype(str)
            + "/"
            + df_player[f"{player_name}-{keys[2]}"].astype(str)
            + "/"
            + df_player[f"{player_name}-{keys[3]}"].astype(str)
            + "/"
            + df_player[f"{player_name}-{keys[4]}"].astype(str)
            + "/"
            + df_player[f"{player_name}-{keys[5]}"].astype(str)
            + "/"
            + df_player[f"{player_name}-{keys[6]}"].astype(str)
            + "/"
            + df_player[f"{player_name}-{keys[7]}"].astype(str)
        )
    df_player = df_player.drop(columns=player_cols)

    # 結合したカラムを加えて melt する
    df = pd.concat([df_common, df_player], axis=1)
    df_melted = df.melt(id_vars=battle_cols, var_name="player")

    # 各プレイヤーのカラムを分離して元に戻す
    df_split = (
        df_melted["value"]
        .str.split("/", expand=True)
        .replace("nan", np.nan)
        .set_axis(keys, axis=1)
        .astype(
            {
                "kill-assist": "int64",
                "kill": "int64",
                "assist": "int64",
                "death": "int64",
                "special": "int64",
                "inked": "int64",
            }
        )
    )

    df = pd.concat([df_melted, df_split], axis=1)

    # win カラムをプレイヤーが勝利したか否かを示す bool とする
    df["team"] = df["player"].map(lambda x: "alpha" if x[0] == "A" else "bravo")
    df["win"] = df["win"] == df["team"]

    # サブ、スペシャル、ブキ種のカラムを追加する
    main_master = m.load_master(m.Master.MAIN_WEAPON)
    df["sub-weapon"] = df["weapon"].map(lambda x: main_master.at[x, "sub-key"])
    df["special-weapon"] = df["weapon"].map(lambda x: main_master.at[x, "special-key"])
    df["weapon-type"] = df["weapon"].map(lambda x: main_master.at[x, "type-key"])

    # 不要なカラムを削除する
    df = df.drop(columns=["value", "team"])

    return df
