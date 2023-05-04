# splat-stat

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

コンテナを起動した状態で以下のコマンドを実行すると、stat.ink の[統計情報ダウンロード](https://dl-stats.stats.ink/splatoon-3/battle-results-csv/)ページから zip ファイルをダウンロードし、データベースの `battles` テーブルに戦績を格納します。 これには数分時間を要します。

```sh
docker compose exec app python scripts/db_init.py
```

また、stat.ink の統計情報には毎日新しいデータが追加されます。 追加分を取得してデータベースに格納するには以下のコマンドを実行します。 これはデータベースの戦績との差分のみをダウンロードするため、既にデータベースに多くの戦績が格納されている場合、初期化よりも効率的です。

```sh
docker compose exec app python scripts/db_update.py
```

### データベースをリセットする

以下のコマンドを実行するとデータベースの `battles` テーブルを空の状態に戻します。

```sh
docker compose exec app python scripts/db_reset.py
```

## マスターデータの取得

以下のコマンドを実行してブキ一覧などのマスターデータを取得します。

```sh
docker compose exec app python scripts/master_update.py
```

## 画像データの取得

以下のコマンドを実行してブキ、サブウェポン、スペシャルウェポンの画像データを取得します。

```sh
docker compose exec app python scripts/image_update.py
```
