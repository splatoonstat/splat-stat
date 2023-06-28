"""
画像データを管理する。
"""
from typing import Optional
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from packages.master import load_master, Master
import packages.definitions as d


def _download_file_to_dir(url: str, dst_dir: str, filename: Optional[str]):
    """
    URL から画像をダウンロードし指定のディレクトリに保存する。
    """
    os.makedirs(dst_dir, exist_ok=True)

    _filename = filename if filename is not None else os.path.basename(url)
    file_path = os.path.join(dst_dir, _filename)

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
    paths = [x.get("src") for x in images]

    # メインウェポン、サブウェポン、スペシャルウェポンの画像パスのみを抽出する
    paths = [x for x in paths if re.match("^/assets/.+/(main|sub|special)/.+\.png", x)]
    # クエリパラメータは除外する
    paths = [x[: x.find("?")] for x in paths]
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


def download_images_from_splatoonwikiorg(delay: int = 3):
    image_dir = d.IMAGES_DIR

    r = requests.get(d.SPLATOONWIKIORG_WEAPON_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table")
    imgs = table.find_all("img")

    main_weapon_imgs = [x for x in imgs if "Weapon Main" in x.get("alt")]
    sub_weapon_imgs = [x for x in imgs if "Weapon Sub" in x.get("alt")]
    special_weapon_imgs = [x for x in imgs if "Weapon Special" in x.get("alt")]

    def imgs_download(imgs: list, master_key: Master, regex: str):
        df = load_master(master_key)
        for img in imgs:
            alt = img.get("alt")
            src = img.get("src")
            url = "https:" + re.sub("60px", "36px", src)
            name = re.search(regex, alt).group(1)
            key = df[df["name-en"] == name].index[0]

            filename = f"{key}.png"
            path = os.path.join(image_dir, filename)

            if not os.path.exists(path):
                time.sleep(delay)
                print(f"download to {path}")
                _download_file_to_dir(url, image_dir, filename)

    imgs_download(main_weapon_imgs, Master.MAIN_WEAPON, "Main (.+) 2D")
    imgs_download(sub_weapon_imgs, Master.SUB_WEAPON, "Sub (.+) Flat")
    imgs_download(special_weapon_imgs, Master.SPECIAL_WEAPON, "Special (.+)\.png")


def download_ability_images_from_splatoonwikiorg(delay: int = 3):
    image_dir = d.IMAGES_DIR

    r = requests.get(d.SPLATOONWIKIORG_ABILITY_URL)
    soup = BeautifulSoup(r.content, "html.parser")
    imgs = soup.select("table.sitecolor-s3 img")
    ability_imgs = [x for x in imgs if "S3 Ability" in x.get("alt")]
    df = load_master(Master.ABILITY)

    for img in ability_imgs:
        alt = img.get("alt")
        src = img.get("src")
        url = "https:" + re.sub("24px", "36px", src)
        name = re.search("S3 Ability (.+)\.png", alt).group(1)
        key = df[df["name-en"] == name].index[0]

        filename = f"{key}.png"
        path = os.path.join(image_dir, filename)

        if not os.path.exists(path):
            time.sleep(delay)
            print(f"download to {path}")
            _download_file_to_dir(url, image_dir, filename)


def get_image_path(key: str) -> str:
    """
    指定した画像の key (e.g. "wakaba") から画像ファイルのパスを返す
    """
    path = f"{d.IMAGES_DIR}/{key}.png"
    if not os.path.exists(path):
        raise ValueError("key not found")
    return path
