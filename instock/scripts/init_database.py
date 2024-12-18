#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging

# 添加项目根目录到系统路径
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

from core.db import init_db


def main():
    """初始化数据库"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    try:
        init_db()
        logging.info("数据库初始化完成")
    except Exception as e:
        logging.error(f"数据库初始化失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
