import re
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
import pandas as pd
import packages.master as m
import packages.definitions as d


def get_ax_size(ax: Axes, fig: Figure):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height


def credit(ax: Axes, fig: Figure, text: str):
    width, height = get_ax_size(ax, fig)
    x, y = 1, -36 / height
    ax.text(
        x=x,
        y=y,
        s=f"{text}\n{d.CREDIT}",
        ha="right",
        va="top",
        fontsize=10,
        transform=ax.transAxes,
    )


def to_players(battles: pd.DataFrame, exclude_A1: bool = True) -> pd.DataFrame:
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
    ]
    player_cols = [x for x in battles.columns if re.compile("^[AB]\d-.+").match(x)]
    if exclude_A1:
        player_cols = [x for x in player_cols if not re.compile("^A1-.+").match(x)]
    keys = [x[3:] for x in battles.columns if re.compile("^A1-.+").match(x)]

    df = battles.melt(id_vars=battle_cols, value_vars=player_cols)
    df["player"] = df["variable"].str[:2]
    df["key"] = df["variable"].str[3:]
    df = df.drop("variable", axis=1)

    def key_to_df(key: str) -> pd.DataFrame:
        return (
            df[df["key"] == key]
            .rename(columns={"value": key})
            .drop(columns=["key"])
            .reset_index(drop=True)
        )

    dfs = [key_to_df(x) for x in keys]
    df = pd.concat(dfs, axis=1)
    df = df.loc[:, ~df.columns.duplicated()]

    # win カラムをプレイヤーが勝利したか否かを示す bool とする
    df["win"] = df.apply(
        lambda row: row["win"][0].lower() == row["player"][0].lower(), axis=1
    )

    # サブ、スペシャル、ブキ種のカラムを追加する
    main_master = m.load_master(m.Master.MAIN_WEAPON)
    df["sub-weapon"] = df["weapon"].map(lambda x: main_master.at[x, "sub-key"])
    df["special-weapon"] = df["weapon"].map(lambda x: main_master.at[x, "special-key"])
    df["weapon-type"] = df["weapon"].map(lambda x: main_master.at[x, "type-key"])

    return df
