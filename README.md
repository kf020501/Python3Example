# Python コンテナ開発テンプレート

Docker 内で動作する Python テンプレート。ホストに Python 不要。

## 前提

- Docker / Docker Compose

## 使い方

```bash
make help    # 利用可能なコマンド一覧
make build   # 初回 or requirements.txt 変更時
make test    # テスト実行
```

## ディレクトリ構成

```
.
├── src/                    # アプリケーションコード
│   ├── app.py              # エントリーポイント
│   └── utils/              # 共通ユーティリティ
│       ├── csv_loader.py
│       ├── logger_setup.py
│       ├── pg_connection.py
│       ├── pg_inserter.py
│       └── sql_loader.py
├── tests/                  # テストコード（src と同構造）
│   ├── test_app.py
│   └── utils/
│       └── test_csv_loader.py
├── config/                 # 設定ファイル（JSON）
│   ├── app.json
│   ├── utils_logger_setup.json
│   └── utils_pg_connection.json
├── docker/
│   └── Dockerfile          # Python 環境定義
├── compose.yml             # Docker Compose 設定
├── requirements.txt        # Python 依存パッケージ（唯一の依存定義）
├── Makefile                # 操作コマンド集（make help で一覧）
├── logs/                   # 実行ログ出力先
└── README.md
```

## 開発ルール

- 依存追加: `requirements.txt` に追記 → `make build`
- 設定追加: `config/` に JSON 配置
- デバッグ: `make debug` → IDE から `localhost:5678` に Attach
