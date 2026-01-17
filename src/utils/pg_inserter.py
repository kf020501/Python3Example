"""
PostgreSQLへのバルクインサートユーティリティ

【使用例】
from utils.pg_connection import connect
from utils.pg_inserter import bulk_insert

conn = connect()
try:
    bulk_insert(conn, "table_name", ["col1", "col2"], [[1, "a"], [2, "b"]])
finally:
    conn.close()
"""

import logging
from typing import Any

from psycopg2 import sql
from psycopg2.extensions import connection as PgConnection

logger = logging.getLogger(__name__)


def bulk_insert(
    conn: PgConnection,
    table_name: str,
    headers: list[str],
    rows: list[list[Any]],
    batch_size: int = 5000,
) -> int:
    """
    データをPostgreSQLにバルクインサートする。

    Args:
        conn: PostgreSQLコネクション
        table_name: テーブル名
        headers: カラム名のリスト
        rows: 挿入するデータの2次元配列
        batch_size: バルクインサートの単位（デフォルト: 5000件）

    Returns:
        挿入した総行数
    """
    if not rows:
        logger.info("挿入するデータがありません")
        return 0

    total_rows = len(rows)
    inserted_count = 0

    # INSERT文の構築
    # INSERT INTO table_name (col1, col2, ...) VALUES (%s, %s, ...)
    columns = sql.SQL(", ").join([sql.Identifier(h) for h in headers])
    placeholders = sql.SQL(", ").join([sql.Placeholder() for _ in headers])
    insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({placeholders})").format(
        table=sql.Identifier(table_name),
        columns=columns,
        placeholders=placeholders,
    )

    logger.info(f"バルクインサート開始: テーブル={table_name}, 総行数={total_rows:,}, バッチサイズ={batch_size:,}")

    with conn.cursor() as cur:
        for batch_start in range(0, total_rows, batch_size):
            batch_end = min(batch_start + batch_size, total_rows)
            batch = rows[batch_start:batch_end]

            # executemanyでバルクインサート
            cur.executemany(insert_query.as_string(conn), batch)
            conn.commit()

            inserted_count += len(batch)
            logger.info(f"進捗: {inserted_count:,} / {total_rows:,} 件完了 ({inserted_count * 100 // total_rows}%)")

    logger.info(f"バルクインサート完了: {inserted_count:,}件挿入")
    return inserted_count
