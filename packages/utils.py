from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
import pandas as pd
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
