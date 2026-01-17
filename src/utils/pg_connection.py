"""
PostgreSQL接続ユーティリティ

【設定ファイル】
config/utils_pg_connection.json

【設定項目】
- host    : ホスト名
- port    : ポート番号
- database: データベース名
- user    : ユーザー名
- password: パスワード

【使用例】
from utils.pg_connection import connect

conn = connect()  # デフォルト設定ファイルを使用
conn = connect("config/custom.json")  # カスタム設定ファイルを使用
try:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
finally:
    conn.close()
"""

import json
from pathlib import Path

import psycopg2
from psycopg2.extensions import connection as PgConnection

# デフォルト設定ファイルパス
DEFAULT_CONFIG_PATH = Path("config/utils_pg_connection.json")


def connect(config_path: Path | str | None = None) -> PgConnection:
    """設定ファイルに基づいてPostgreSQLコネクションを作成する。"""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    with path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    return psycopg2.connect(
        host=config["host"],
        port=config["port"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
    )
