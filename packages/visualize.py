import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from packages.japanize import japanize
from packages.i18n import Locale, Translator
import packages.definitions as d
import packages.utils as u


def xmatch_mode_breakdown(battles: pd.DataFrame, locale: Locale = Locale.JA):
    print(f"バトル数: {len(battles)}")
    mode_count = battles["mode"].value_counts().reset_index().set_axis(["mode", "count"], axis=1)
    mode_count["order"] = mode_count["mode"].map(lambda x: d.MODE_ORDER.index(x))
    mode_count = mode_count.sort_values("order").drop(columns="order")

    i18n = Translator(locale)
    i18n.add("breakdown", "ルール内訳", "Breakdown of battles")
    i18n.add("battle_num", "バトル数", "Number of battles")

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
        title=i18n.t("breakdown"),
        xlabel=i18n.t("battle_num"),
        ylabel="",
        yticklabels=map(lambda x: i18n.t(x), d.MODE_ORDER),
        xlim=(0, mode_count["count"].max() * 1.2),
    )
    u.credit(g.ax, g.fig, i18n.t_data_duration(battles))
    plt.show()


def xmatch_power_distribution(battles: pd.DataFrame, locale: Locale = Locale.JA):
    invalid_battle_num = len(battles[battles["power"].isna()])
    print(f"パワー不明バトル数: {invalid_battle_num}")
    power_agg = battles["power"].describe()

    i18n = Translator(locale)
    i18n.add("title", "集計した stat.ink 投稿者のXパワー分布（バトル数ベース）", "X Power distribution of stat.ink users (based on number of battles)")
    i18n.add("power", "Xパワー", "X Power")
    i18n.add("battle_num", "バトル数", "Number of battles")
    i18n.add("mean", "平均値", "Average")
    i18n.add("sd", "標準偏差", "Standard deviation")

    g = sns.displot(
        data=battles,
        x="power",
        height=5,
        aspect=1.5,
    )
    ax = g.ax
    ax.set(
        title=i18n.t("title"),
        xlabel=i18n.t("power"),
    )
    ax.text(
        0.97,
        0.97,
        f"{i18n.t('battle_num')}: {round(power_agg.loc['count'])}\n{i18n.t('mean')}: {round(power_agg.loc['mean'])}\n{i18n.t('sd')}: {round(power_agg.loc['std'])}\n25%: {round(power_agg.loc['25%'])}\n50%: {round(power_agg.loc['50%'])}\n75%: {round(power_agg.loc['75%'])}",
        ha="right",
        va="top",
        fontsize=10,
        linespacing=1.8,
        transform=ax.transAxes,
    )
    u.credit(g.ax, g.fig, i18n.t_data_duration(battles))
    plt.show()


def splatfest_challenge_power_distribution(battles: pd.DataFrame, locale: Locale = Locale.JA):
    invalid_battle_num = len(battles[battles["power"].isna()])
    print(f"パワー不明バトル数: {invalid_battle_num}")
    power_agg = battles["power"].describe()

    sns.set_theme()
    japanize()

    i18n = Translator(locale)
    i18n.add("title", "集計した stat.ink 投稿者のフェスパワー分布（バトル数ベース）", "Splatfest power distribution of stat.ink users (based on number of battles)")
    i18n.add("power", "フェスパワー", "Splatfest power")
    i18n.add("battle_num", "バトル数", "Number of battles")
    i18n.add("mean", "平均値", "Average")
    i18n.add("sd", "標準偏差", "Standard deviation")

    g = sns.displot(
        data=battles,
        x="power",
        height=5,
        aspect=1.5,
    )
    ax = g.ax
    ax.set(
        title=i18n.t("title"),
        xlabel=i18n.t("power"),
    )
    ax.text(
        0.97,
        0.97,
        f"{i18n.t('battle_num')}: {round(power_agg.loc['count'])}\n{i18n.t('mean')}: {round(power_agg.loc['mean'])}\n{i18n.t('sd')}: {round(power_agg.loc['std'])}\n25%: {round(power_agg.loc['25%'])}\n50%: {round(power_agg.loc['50%'])}\n75%: {round(power_agg.loc['75%'])}",
        ha="right",
        va="top",
        fontsize=10,
        linespacing=1.8,
        transform=ax.transAxes,
    )
    u.credit(g.ax, g.fig, i18n.t_data_duration(battles))
    plt.show()
