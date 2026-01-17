#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ロガー初期化を提供するユーティリティモジュール

Args:
    logger_cfg (Dict[str, Any]):
        設定項目をまとめた辞書。以下のキーを解釈する：
        - level (str): デフォルトのログレベル (デフォルト: "INFO")
        - console_output (dict):
            - enabled (bool): コンソール出力を有効にするかどうか (デフォルト: True)
            - level (str): コンソール用ログレベル (デフォルト: root level または level)
        - file_output (dict):
            - enabled (bool): ファイル出力を有効にするかどうか (デフォルト: False)
            - level (str): ファイル用ログレベル (デフォルト: root level または level)
            - output_directory (str): ログファイルを保存するディレクトリ (デフォルト: "logs")
            - file_prefix (str): ログファイル名の接頭辞 (デフォルト: 空文字)
"""
import logging
import sys
import json
from pathlib import Path
from datetime import datetime

def setup_logger(logger_cfg):
    # ルート設定レベル
    config_root_name = logger_cfg.get('level', 'INFO').upper()
    config_root_level = getattr(logging, config_root_name, logging.INFO)

    # コンソール設定
    console_cfg = logger_cfg.get('console_output', {})
    console_enabled = console_cfg.get('enabled', True)
    console_name = console_cfg.get('level', config_root_name).upper()
    console_level = getattr(logging, console_name, config_root_level)

    # ファイル設定
    file_cfg = logger_cfg.get('file_output', {})
    file_enabled = file_cfg.get('enabled', False)
    file_name = file_cfg.get('level', config_root_name).upper()
    file_level = getattr(logging, file_name, config_root_level)
    output_directory = file_cfg.get('output_directory', 'logs')
    file_prefix = file_cfg.get('file_prefix', '')

    # フォーマッタ作成
    fmt = '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    # ルートロガー取得
    logger = logging.getLogger()

    # ルートロガーのレベルを、各ハンドラの最小レベルか config_root_level のいずれか低い方に設定
    handler_levels = []
    if console_enabled:
        handler_levels.append(console_level)
    if file_enabled:
        handler_levels.append(file_level)
    if handler_levels:
        root_level = min(handler_levels)
    else:
        root_level = config_root_level
    logger.setLevel(root_level)

    # コンソールハンドラ
    if console_enabled:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(console_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    # ファイルハンドラ
    if file_enabled:
        base_dir = Path(__file__).resolve().parent
        log_dir = base_dir / output_directory
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = log_dir / f"{file_prefix}{timestamp}.log"
        fh = logging.FileHandler(log_path, encoding='utf-8')
        fh.setLevel(file_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # 設定内容を1行JSONでデバッグ出力
    logger.debug(json.dumps(logger_cfg, ensure_ascii=False, separators=(',',':')))
    logger.debug("Logger initialized successfully")
