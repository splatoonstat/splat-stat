import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from packages.japanize import japanize
import packages.i18n as i18n
import packages.definitions as d
import packages.utils as u


def xmatch_mode_breakdown(battles: pd.DataFrame, locale: i18n.Locale = i18n.Locale.JA):
    print(f"バトル数: {len(battles)}")
    mode_count = battles["mode"].value_counts().reset_index().set_axis(["mode", "count"], axis=1)
    mode_count["order"] = mode_count["mode"].map(lambda x: d.MODE_ORDER.index(x))
    mode_count = mode_count.sort_values("order").drop(columns="order")

    translations = i18n.get_translations(custom_translation_df=pd.DataFrame([
        { "key": "breakdown", "name-ja": "ルール内訳", "name-en": "Breakdown of battles" },
        { "key": "battle_num", "name-ja": "バトル数", "name-en": "Number of battles" },
    ]), locale=locale)

    sns.set_theme()
    japanize()

    g = sns.catplot(
        data=mode_count,
        x="count",
        y="mode",
        kind="bar",
        color="b",
        alpha=0.8,
        height=3,
        aspect=2,
    )
    ax = g.ax
    ax.bar_label(ax.containers[0], fmt="%.0f", padding=6)
    ax.set(
        title=translations["breakdown"],
        xlabel=translations["battle_num"],
        ylabel="",
        yticklabels=map(lambda x: translations[x], d.MODE_ORDER),
        xlim=(0, mode_count["count"].max() * 1.2),
    )
    u.credit(g.ax, g.fig, i18n.data_to_duration_str(battles, locale))
    plt.show()


def xmatch_power_distribution(battles: pd.DataFrame, locale: i18n.Locale = i18n.Locale.JA):
    invalid_battle_num = len(battles[battles["power"].isna()])
    print(f"パワー不明バトル数: {invalid_battle_num}")
    power_agg = battles["power"].describe()

    translations = i18n.get_translations(custom_translation_df=pd.DataFrame([
        { "key": "title", "name-ja": "集計した stat.ink 投稿者のXパワー分布（バトル数ベース）", "name-en": "X Power distribution of stat.ink users (based on number of battles)" },
        { "key": "power", "name-ja": "Xパワー", "name-en": "X Power" },
        { "key": "battle_num", "name-ja": "バトル数", "name-en": "Number of battles" },
        { "key": "mean", "name-ja": "平均値", "name-en": "Average" },
        { "key": "sd", "name-ja": "標準偏差", "name-en": "Standard deviation" },
    ]), locale=locale)

    g = sns.displot(
        data=battles,
        x="power",
        height=5,
        aspect=1.5,
    )
    ax = g.ax
    ax.set(
        title=translations["title"],
        xlabel=translations["power"],
    )
    ax.text(
        0.97,
        0.97,
        f"{translations['battle_num']}: {round(power_agg.loc['count'])}\n{translations['mean']}: {round(power_agg.loc['mean'])}\n{translations['sd']}: {round(power_agg.loc['std'])}\n25%: {round(power_agg.loc['25%'])}\n50%: {round(power_agg.loc['50%'])}\n75%: {round(power_agg.loc['75%'])}",
        ha="right",
        va="top",
        fontsize=10,
        linespacing=1.8,
        transform=ax.transAxes,
    )
    u.credit(g.ax, g.fig, i18n.data_to_duration_str(battles, locale))
    plt.show()


def splatfest_challenge_power_distribution(battles: pd.DataFrame, locale: i18n.Locale = i18n.Locale.JA):
    invalid_battle_num = len(battles[battles["power"].isna()])
    print(f"パワー不明バトル数: {invalid_battle_num}")
    power_agg = battles["power"].describe()

    sns.set_theme()
    japanize()

    translations = i18n.get_translations(custom_translation_df=pd.DataFrame([
        { "key": "title", "name-ja": "集計した stat.ink 投稿者のフェスパワー分布（バトル数ベース）", "name-en": "Splatfest power distribution of stat.ink users (based on number of battles)" },
        { "key": "power", "name-ja": "フェスパワー", "name-en": "Splatfest power" },
        { "key": "battle_num", "name-ja": "バトル数", "name-en": "Number of battles" },
        { "key": "mean", "name-ja": "平均値", "name-en": "Average" },
        { "key": "sd", "name-ja": "標準偏差", "name-en": "Standard deviation" },
    ]), locale=locale)

    g = sns.displot(
        data=battles,
        x="power",
        height=5,
        aspect=1.5,
    )
    ax = g.ax
    ax.set(
        title=translations["title"],
        xlabel=translations["power"],
    )
    ax.text(
        0.97,
        0.97,
        f"{translations['battle_num']}: {round(power_agg.loc['count'])}\n{translations['mean']}: {round(power_agg.loc['mean'])}\n{translations['sd']}: {round(power_agg.loc['std'])}\n25%: {round(power_agg.loc['25%'])}\n50%: {round(power_agg.loc['50%'])}\n75%: {round(power_agg.loc['75%'])}",
        ha="right",
        va="top",
        fontsize=10,
        linespacing=1.8,
        transform=ax.transAxes,
    )
    u.credit(g.ax, g.fig, i18n.data_to_duration_str(battles, locale))
    plt.show()
