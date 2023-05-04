import os
import matplotlib
from matplotlib import font_manager
from distutils.version import LooseVersion

import packages.definitions as d

FONT_NAME = "IPAexGothic"


def japanize():
    """
    matplotlib に日本語フォントを設定する
    """
    font_dirs = [d.FONTS_DIR]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    is_support_createFontList = LooseVersion(matplotlib.__version__) < "3.2"
    if is_support_createFontList:
        font_list = font_manager.createFontList(font_files)
        font_manager.fontManager.ttflist.extend(font_list)
    else:
        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)
    matplotlib.rc("font", family=FONT_NAME)
