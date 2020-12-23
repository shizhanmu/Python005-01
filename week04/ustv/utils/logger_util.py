#!/usr/bin/env python
# coding: utf-8
import colorlog
import logging
from pathlib import Path

__all__ = ['logger']

BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / 'transfer.log'

formatter = colorlog.StreamHandler()
formatter.setFormatter(
    colorlog.ColoredFormatter(
        fmt='%(log_color)s[%(levelname)s] [%(threadName)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
    )
)
formatter.setLevel('INFO')
handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(formatter)
logger.addHandler(handler)
logger.setLevel("DEBUG")