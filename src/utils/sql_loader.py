"""
SQLファイル読み込みユーティリティ

【概要】
- src/sql ディレクトリからSQLファイルを読み込む
- ファイル名のみ指定してSQL文字列を取得

【使用例】
from utils.sql_loader import load_sql

sql = load_sql("select_users")  # src/sql/select_users.sql を読み込み
sql = load_sql("select_users.sql")  # .sql付きでもOK
"""

from pathlib import Path

# SQLファイル格納ディレクトリ
SQL_BASE_DIR = Path("src/sql")


def load_sql(filename: str, *, encoding: str = "utf-8") -> str:
    """
    SQLファイルを読み込んで文字列を返す。

    Args:
        filename: SQLファイル名（.sql拡張子は省略可）
        encoding: ファイルの文字エンコーディング（デフォルト: utf-8）

    Returns:
        SQLファイルの内容

    Raises:
        FileNotFoundError: ファイルが見つからない場合
    """
    # .sql拡張子がなければ追加
    if not filename.endswith(".sql"):
        filename = f"{filename}.sql"

    sql_path = SQL_BASE_DIR / filename

    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    return sql_path.read_text(encoding=encoding)
