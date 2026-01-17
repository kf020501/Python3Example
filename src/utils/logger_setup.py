#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ロガー初期化を提供するユーティリティモジュール

【設定ファイル】
config/utils_logger_setup.json

【設定項目】
- level        : ログレベル (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- console      : コンソール出力の有無 (true/false)
- console_level: コンソール出力レベル (省略時はlevelを使用)
- file         : ファイル出力の有無 (true/false)
- file_level   : ファイル出力レベル (省略時はlevelを使用)
- file_dir     : ログファイル出力ディレクトリ (file=true時は必須)
- file_prefix  : ログファイル名プレフィックス
- fmt          : ログフォーマット
- datefmt      : 日時フォーマット

【使用例】
from utils.logger_setup import setup_logger

logger = setup_logger()  # デフォルト設定ファイルを使用
logger = setup_logger("config/custom.json")  # カスタム設定ファイルを使用
logger.info("メッセージ")
"""
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# デフォルト設定ファイルパス
DEFAULT_CONFIG_PATH = Path("config/utils_logger_setup.json")


def setup_logger(config_path: Path | str | None = None) -> logging.Logger:
    """設定ファイルに基づいてロガーを初期化する。"""
    # 設定ファイル読み込み
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    with path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    level = config["level"]
    console = config["console"]
    console_level = config.get("console_level")
    file = config["file"]
    file_level = config.get("file_level")
    file_dir = config.get("file_dir")
    file_prefix = config["file_prefix"]
    fmt = config["fmt"]
    datefmt = config["datefmt"]

    # ルートロガー取得
    logger = logging.getLogger()

    # 既存ハンドラをクリアして二重出力を防ぐ
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    # レベル値取得
    root_level = getattr(logging, level.upper())
    console_lvl = getattr(logging, (console_level or level).upper())
    file_lvl = getattr(logging, (file_level or level).upper())

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    handler_levels: list[int] = []

    if console:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(console_lvl)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        handler_levels.append(console_lvl)

    if file:
        log_dir = Path(file_dir).expanduser()
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = log_dir / f"{file_prefix}{timestamp}_{os.getpid()}.log"
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel(file_lvl)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        handler_levels.append(file_lvl)

    logger.setLevel(min(handler_levels) if handler_levels else root_level)
    return logger
