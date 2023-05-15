"""
データベースを管理する。
"""
import os
import io
import re
import time
import zipfile
import shutil
import datetime as dt
import requests
import pandas as pd
from bs4 import BeautifulSoup
import packages.db as db
import packages.definitions as d


def _get_csv_file_paths(current_path: str, delay: int = 3) -> list[str]:
    """
    stat.ink のダウンロードページを巡回して、
    csv ファイルの pathname (URL の最初の `/` とその後に続く URL のパス) のリストを返す。
    """
    # URL へアクセスする
    print(f"request to {current_path}")
    url = f"{d.STATINK_DOWNLOAD_BASE_URL}{current_path}"
    r = requests.get(url)

    # HTML をパースしてリンクを収集する
    soup = BeautifulSoup(r.content, "html.parser")
    anchors = soup.find_all("a")
    paths = [x.get("href") for x in anchors]

    # 収集したリンクから csv ファイルのリストを抽出する
    csv_paths = [x for x in paths if re.match(rf"{current_path}.+\.csv", x)]
    # 収集したリンクから下層ディレクトリのリストを抽出する
    dir_paths = [x for x in paths if re.match(rf"{current_path}.+/", x)]

    # 下層ディレクトリがあれば再帰的に csv ファイルを取得する
    for dir_path in dir_paths:
        time.sleep(delay)
        nested_csv_paths = _get_csv_file_paths(dir_path, delay)
        csv_paths.extend(nested_csv_paths)

    return csv_paths


def _path_to_filename_without_ext(path: str) -> str:
    """
    ファイルパスから拡張子を除外したファイル名を取得する。
    """
    filename = os.path.basename(path)
    return os.path.splitext(filename)[0]


def _csv_path_to_date(csv_path: str) -> dt.date:
    """
    csv ファイルのファイル名から date オブジェクトを生成して返す。
    """
    date_str = _path_to_filename_without_ext(csv_path)
    return dt.date.fromisoformat(date_str)


def _check_csv_exist(csv_path: str, table_name: str) -> bool:
    """
    csv ファイルのファイル名の date のデータが DB に存在していれば True を返す。
    """
    date = _csv_path_to_date(csv_path)
    battles = list(
        db.execute_sql(sql=f"select * from {table_name} where date = '{date}' limit 1")
    )
    return len(battles) > 0


def _save_battles(csv_path: str):
    """
    csv_path の戦績データを DB へ書き込む。
    """
    # csv を読み込む
    battles = pd.read_csv(csv_path)

    # データを扱いやすいように加工する
    date = _csv_path_to_date(csv_path)
    battles.insert(2, "date", date)
    battles = battles.rename(columns={"# season": "season"})
    battles["period"] = pd.to_datetime(battles["period"])
    battles["date"] = pd.to_datetime(battles["date"])
    battles["knockout"] = battles["knockout"].astype("bool")

    # DB へ書き込む
    db.save_battles(battles=battles)


def update_battles(delay: int = 3):
    """
    stat.ink のダウンロードページから戦績の csv ファイルのリストを取得し、
    未保存のデータを取得して DB へ書き込む。
    """
    csv_paths = _get_csv_file_paths(d.STATINK_DOWNLOAD_BATTLE_PATH)
    non_existing_files = [x for x in csv_paths if not _check_csv_exist(x, "battles")]

    # csv をダウンロードして DB へ書き込む
    file_num = len(non_existing_files)
    for i, path in enumerate(non_existing_files):
        time.sleep(delay)
        url = d.STATINK_DOWNLOAD_BASE_URL + path
        print(f"({i+1}/{file_num}) download {url}")
        _save_battles(url)


def init_battles():
    """
    stat.ink のダウンロードページから戦績の zip ファイルを取得し、
    解凍してできた csv ファイルからデータを DB へ書き込む。
    """
    zip_url = d.STATINK_DOWNLOAD_BATTLE_ZIP_URL
    extract_dir = d.WORK_DIR
    zip_filename = _path_to_filename_without_ext(zip_url)
    dirname = f"{extract_dir}/{zip_filename}"

    # 展開されたディレクトリが存在しなければ zip ファイルをダウンロードして解凍する
    if not os.path.exists(dirname):
        print(f"request to {zip_url}")
        with (
            requests.get(zip_url) as res,
            io.BytesIO(res.content) as bytes_io,
            zipfile.ZipFile(bytes_io) as zip,
        ):
            zip.extractall(extract_dir)

    # 展開されたディレクトリ内の csv ファイルから、未保存のファイルのリストを抽出する
    csv_paths = [f"{dirname}/{x}" for x in os.listdir(path=dirname)]
    non_existing_files = [x for x in csv_paths if not _check_csv_exist(x, "battles")]

    # csv を読み込み DB へ書き込む
    file_num = len(non_existing_files)
    for i, path in enumerate(non_existing_files):
        print(f"({i+1}/{file_num}) save {path}")
        _save_battles(path)

    # 展開されたディレクトリを削除する
    shutil.rmtree(dirname)


def reset_battles():
    """
    battles テーブルを削除し空のテーブルを作り直す
    """
    # DB のテーブルを削除する
    db.execute_sql("drop table if exists battles")

    # DB に空のテーブルを作成する
    dirname = d.INIT_DIR
    sql_files = [f"{dirname}/{x}" for x in os.listdir(dirname)]

    for sql_file in sql_files:
        with open(sql_file) as file:
            db.execute_sql(file.read())


def _save_works(csv_path: str):
    """
    csv_path のサーモンランデータを DB へ書き込む。
    """
    # csv を読み込む
    works = pd.read_csv(csv_path)

    # データを扱いやすいように加工する
    date = _csv_path_to_date(csv_path)
    works.insert(2, "date", date)
    works = works.rename(columns={"# season": "season"})
    works["rotation"] = pd.to_datetime(works["rotation"])
    works["date"] = pd.to_datetime(works["date"])
    works["cleared"] = works["cleared"].astype("bool")
    works["cleared-extra"] = works["cleared-extra"].astype("bool")

    # DB へ書き込む
    db.save_works(works=works)


def update_works(delay: int = 3):
    """
    stat.ink のダウンロードページからサーモンランの csv ファイルのリストを取得し、
    未保存のデータを取得して DB へ書き込む。
    """
    csv_paths = _get_csv_file_paths(d.STATINK_DOWNLOAD_SALMON_PATH)
    non_existing_files = [x for x in csv_paths if not _check_csv_exist(x, "works")]

    # csv をダウンロードして DB へ書き込む
    file_num = len(non_existing_files)
    for i, path in enumerate(non_existing_files):
        time.sleep(delay)
        url = d.STATINK_DOWNLOAD_BASE_URL + path
        print(f"({i+1}/{file_num}) download {url}")
        _save_works(url)


def init_works():
    """
    stat.ink のダウンロードページからサーモンランの zip ファイルを取得し、
    解凍してできた csv ファイルからデータを DB へ書き込む。
    """
    zip_url = d.STATINK_DOWNLOAD_SALMON_ZIP_URL
    extract_dir = d.WORK_DIR
    zip_filename = _path_to_filename_without_ext(zip_url)
    dirname = f"{extract_dir}/{zip_filename}"

    # 展開されたディレクトリが存在しなければ zip ファイルをダウンロードして解凍する
    if not os.path.exists(dirname):
        print(f"request to {zip_url}")
        with (
            requests.get(zip_url) as res,
            io.BytesIO(res.content) as bytes_io,
            zipfile.ZipFile(bytes_io) as zip,
        ):
            zip.extractall(extract_dir)

    # 展開されたディレクトリ内の csv ファイルから、未保存のファイルのリストを抽出する
    csv_paths = [f"{dirname}/{x}" for x in os.listdir(path=dirname)]
    non_existing_files = [x for x in csv_paths if not _check_csv_exist(x, "works")]

    # csv を読み込み DB へ書き込む
    file_num = len(non_existing_files)
    for i, path in enumerate(non_existing_files):
        print(f"({i+1}/{file_num}) save {path}")
        _save_works(path)

    # 展開されたディレクトリを削除する
    shutil.rmtree(dirname)


def reset_works():
    """
    works テーブルを削除し空のテーブルを作り直す
    """
    # DB のテーブルを削除する
    db.execute_sql("drop table if exists works")

    # DB に空のテーブルを作成する
    dirname = d.INIT_DIR
    sql_files = [f"{dirname}/{x}" for x in os.listdir(dirname)]

    for sql_file in sql_files:
        with open(sql_file) as file:
            db.execute_sql(file.read())
