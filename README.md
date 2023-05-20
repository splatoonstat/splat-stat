# splat-stat

> stat.ink の統計情報を利用した Splatoon3 のデータ分析・ビジュアライゼーション環境です。

## 事前準備

[Docker](https://docs.docker.jp/) がインストールされている必要があります。 各自のプラットフォームに対応する Docker をインストールしてください。

## コンテナを起動する

以下のコマンドを実行するとコンテナがバックグラウンドで起動します。

```sh
docker compose up --detach
```

コンテナを終了するには以下のコマンドを実行します。

```sh
docker compose down
```

## データベースを準備する

### 戦績データを登録する

コンテナを起動した状態で以下のコマンドを実行すると、stat.ink の[統計情報ダウンロード](https://dl-stats.stats.ink/splatoon-3/battle-results-csv/)ページから zip ファイルをダウンロードし、データベースの `battles` テーブルに戦績を格納します。 これには数分時間を要します。

```sh
docker compose exec app python scripts/init_battles.py
```

また、stat.ink の統計情報には毎日新しいデータが追加されます。 追加分を取得してデータベースに格納するには以下のコマンドを実行します。 これはデータベースの戦績との差分のみをダウンロードするため、既にデータベースに多くの戦績が格納されている場合、初期化よりも効率的です。

```sh
docker compose exec app python scripts/update_battles.py
```

#### テーブルをリセットする

以下のコマンドを実行するとデータベースの `battles` テーブルを空の状態に戻します。

```sh
docker compose exec app python scripts/reset_battles.py
```

### サーモンランデータを登録する

サーモンランデータは `works` テーブルを使用します。 管理方法は戦績データと同様です。

```sh
# 初期データの登録
docker compose exec app python scripts/init_works.py

# データの更新
docker compose exec app python scripts/update_works.py

# テーブルのリセット
docker compose exec app python scripts/reset_works.py
```

## マスターデータの取得

以下のコマンドを実行してブキ一覧などのマスターデータを取得します。 取得したデータは `masters` ディレクトリに格納されます。

```sh
docker compose exec app python scripts/update_master.py
```

## 画像データの取得

以下のコマンドを実行してブキ、サブウェポン、スペシャルウェポンの画像データを取得します。 取得したデータは `images` ディレクトリに格納されます。

```sh
docker compose exec app python scripts/update_image.py
```
