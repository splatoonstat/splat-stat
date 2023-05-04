import os
import re
import time
import requests
from bs4 import BeautifulSoup
import src.definitions as d


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

    r = requests.get(d.STATINK_API_WEAPON_INFO_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    images = soup.select("tr img")
    paths = list(map(lambda x: x.get("src"), images))
    paths = [x for x in paths if re.match("^/assets/.+/(main|sub|special)/.+\.png", x)]
    paths = list(map(lambda x: x[: x.find("?")], paths))
    paths = list(set(paths))
    paths = [
        x for x in paths if not os.path.exists(f"{image_dir}/{os.path.basename(x)}")
    ]
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
