import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "resources" / "config.json"


def read_config(path: Path) -> dict:
    """JSON設定を読み込む。

    Args:
        path: 設定JSONのパス

    Returns:
        読み込んだ設定の辞書
    """
    # JSON設定を読み込む。
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Config not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON: {path}") from exc


def load_max_from_json(path: Path) -> int:
    """設定の "max" を読み込んで数値として返す。

    Args:
        path: 設定JSONのパス

    Returns:
        読み込んだ上限値
    """
    # 設定の "max" を読み込んで数値として返す。
    config = read_config(path)
    max_value = config.get("max")
    if max_value is None:
        raise RuntimeError(f"Missing 'max' in {path}")
    return int(max_value)


def fizz_buzz(value: int) -> str:
    """FizzBuzz判定の結果文字列を返す。

    Args:
        value: 判定対象の数値

    Returns:
        FizzBuzzの結果文字列
    """
    # FizzBuzz判定ロジック。
    if value % 15 == 0:
        return "FizzBuzz"
    if value % 3 == 0:
        return "Fizz"
    if value % 5 == 0:
        return "Buzz"
    return str(value)


def main() -> None:
    """JSONの上限値を読み込み、1..max を出力する。"""
    # JSONの上限値を読み込み、1..max を出力する。
    max_value = load_max_from_json(CONFIG_PATH)
    for i in range(1, max_value + 1):
        print(fizz_buzz(i))


if __name__ == "__main__":
    main()
