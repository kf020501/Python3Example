# Python サンプルPJ 設計メモ

## 目的
- Docker コンテナ内だけで実行できる Python 開発テンプレートを提供
- Makefile から一通りの操作が可能
- ログや依存キャッシュをホストに残し、再実行を高速化
- Java 版と同じ「操作体験」を維持

## プロジェクト構成（案）
- `temp/PythonExample/`
  - `README.md` 使用方法と前提、図解
  - `Makefile` 操作コマンド
  - `requirements.txt` 依存定義（Single Source of Truth）
  - `compose.yml` コンテナ構成
  - `docker/` Dockerfile
  - `src/` 実装コード
  - `tests/` pytest
  - `logs/` 実行ログ
  - `.venv/` 依存（コンテナイメージに同梱する前提）

## 依存管理方針
- `requirements.txt` を依存定義の単一ソースにする
- ツールは `pip` + `venv` を固定
  - 依存はコンテナイメージ内でインストールし、`.venv/` を同梱する

## Docker 方針
- 開発用イメージを `docker/Dockerfile` で定義（`ubuntu:24.04` ベース）
- `compose.yml` で `python` サービスを定義
- `UID/GID` を環境変数として渡し、ホスト権限で実行
- `working_dir` は `/workspace`
- コードはコンテナに含めず、ホストから bind mount
- `logs/` を bind mount
  - `.venv/` はイメージに含める

## Makefile（案）
- `help` ターゲットで一覧表示
- `build` でイメージ構築
- `prepare` で `logs/` 作成
- `test` で pytest 実行（ログ保存）
- `run` でアプリ実行
- `debug` でデバッグ待受（`debugpy`）
- `shell` でコンテナ内シェル
- `clean` で生成物削除

## サンプル実装（案）
- Java 版と同様に FizzBuzz を実装
- 設定は JSON で `src/resources/config.json`
- 1..max を出力する CLI
- テストは `tests/test_app.py` で `fizz_buzz` を検証

## README 構成（案）
- 前提（Docker 必須、Python はコンテナのみ）
- 使い方（Makefile / 直接 docker compose）
- アーキテクチャ図（ホスト/コンテナ/依存キャッシュ）
- デバッグ手順（debugpy, 5678）
- ディレクトリ構成

## ディレクトリ構成の一般論（案）
サンプル用途なら深い階層は不要なため、`src/` 直下にモジュールを置く構成とする。

### `src/` 直下にモジュールを置く最小構成
```
PythonExample/
├── src/
│   ├── app.py
│   └── resources/
│       └── config.json
├── tests/
│   └── test_app.py
├── requirements.txt
├── docker/
│   └── Dockerfile
├── compose.yml
├── logs/
├── Makefile
└── README.md
```

## build成果物について
インタプリタ言語のため、サンプル用途では配布用成果物は作成しない前提とする。

## Docstring スタイル検討（案）
Python では主に Google スタイルと NumPy スタイルが広く使われる。
ここでは両者の特徴と選定観点を整理する。

### Google スタイル
```
def fizz_buzz(value: int) -> str:
    """FizzBuzzの結果文字列を返す。

    Args:
        value: 判定対象の数値

    Returns:
        FizzBuzzの結果文字列
    """
```

特徴:
- セクションが短く、読みやすい
- IDE での表示やレビュー時の視認性が高い
- 仕様がシンプルで学習コストが低い

### NumPy スタイル
```
def fizz_buzz(value: int) -> str:
    """FizzBuzzの結果文字列を返す。

    Parameters
    ----------
    value : int
        判定対象の数値

    Returns
    -------
    str
        FizzBuzzの結果文字列
    """
```

特徴:
- 研究系・数値系の文脈で広く使われる
- 長い説明を構造化しやすい
- Sphinx などでのドキュメント生成に向く

### 比較観点
- 簡潔さ: Google が優位
- 詳細記述・表現力: NumPy が優位
- 初学者の読みやすさ: Google が優位
- 既存エコシステムとの相性: 利用領域次第

### サンプルPJとしての方針
本テンプレートは学習用途・小規模用途を想定しているため、
簡潔で読みやすい Google スタイルを採用する。

## マウント設計（案）
bind mount によってホストのコードをそのままコンテナで実行する。

### マウント対象
- `.` → `/workspace`（コード・設定・テスト）
- `./logs` → `/workspace/logs`（実行ログ）

### イメージに含めるもの
- `.venv/`（依存はイメージ内に同梱）

### コンテナ内パスの想定
- `/workspace/src` を実行対象
- `/workspace/tests` をテスト対象
- `/workspace/logs` にログ出力
