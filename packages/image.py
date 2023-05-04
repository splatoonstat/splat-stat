"""
画像データを管理する。
"""
import os
import re
import time
import requests
from bs4 import BeautifulSoup
import packages.definitions as d


def _download_file_to_dir(url: str, dst_dir: str):
    """
    URL から画像をダウンロードし指定のディレクトリに保存する。
    """
    os.makedirs(dst_dir, exist_ok=True)

    file_path = os.path.join(dst_dir, os.path.basename(url))
    try:
        r = requests.get(url)
        with open(file_path, mode="wb") as file:
            file.write(r.content)
    except Exception as e:
        print(e)


def download_images(delay: int = 3):
    """
    メインウェポン、サブウェポン、スペシャルウェポンの画像をダウンロードする
    """
    image_dir = d.IMAGES_DIR

    # API 情報へアクセスして画像パスを収集する
    r = requests.get(d.STATINK_API_WEAPON_INFO_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    images = soup.select("tr img")
    paths = list(map(lambda x: x.get("src"), images))

    # メインウェポン、サブウェポン、スペシャルウェポンの画像パスのみを抽出する
    paths = [x for x in paths if re.match("^/assets/.+/(main|sub|special)/.+\.png", x)]
    # クエリパラメータは除外する
    paths = list(map(lambda x: x[: x.find("?")], paths))
    # 重複した画像パスは除外する
    paths = list(set(paths))
    # 既に取得済みの画像は除外する
    paths = [
        x for x in paths if not os.path.exists(f"{image_dir}/{os.path.basename(x)}")
    ]

    # 画像をダウンロードしてディレクトリに保存する
    file_num = len(paths)
    for i, path in enumerate(paths):
        time.sleep(delay)
        url = d.STATINK_BASE_URL + path
        print(f"({i+1}/{file_num}) download {url}")
        _download_file_to_dir(url, image_dir)


def get_image_path(key: str) -> str:
    """
    指定した画像の key (e.g. "wakaba") から画像ファイルのパスを返す
    """
    path = f"{d.IMAGES_DIR}/{key}.png"
    if not os.path.exists(path):
        raise ValueError("key not found")
    return path
