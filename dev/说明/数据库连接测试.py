#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库连接测试脚本
用于诊断数据库连接和表结构问题
"""

import os
import sys
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 添加项目路径
cpath_current = os.path.dirname(os.path.dirname(__file__))
sys.path.append(cpath_current)


def test_database_connection():
    """测试数据库连接"""
    try:
        from instock.core.db import get_engine, init_db, DatabaseSession
        from instock.core.db.models.spot import StockSpot
        from instock.core.db.models.etf import StockETFSpot

        logging.info("开始测试数据库连接...")

        # 获取数据库引擎
        engine = get_engine()
        logging.info(f"数据库引擎: {engine}")

        # 测试连接
        with engine.connect() as conn:
            logging.info("数据库连接成功!")

            # 测试查询
            result = conn.execute("SELECT 1")
            logging.info(f"测试查询结果: {result.fetchone()}")

            # 检查数据库版本
            result = conn.execute("SELECT VERSION()")
            logging.info(f"数据库版本: {result.fetchone()}")

        # 测试表是否存在
        logging.info("检查数据库表...")
        with DatabaseSession() as db:
            # 检查StockSpot表
            try:
                count = db.query(StockSpot).count()
                logging.info(f"StockSpot表记录数: {count}")
            except Exception as e:
                logging.error(f"StockSpot表查询失败: {e}")

            # 检查StockETFSpot表
            try:
                count = db.query(StockETFSpot).count()
                logging.info(f"StockETFSpot表记录数: {count}")
            except Exception as e:
                logging.error(f"StockETFSpot表查询失败: {e}")

        logging.info("数据库连接测试完成!")
        return True

    except Exception as e:
        logging.error(f"数据库连接测试失败: {e}")
        import traceback

        logging.error(f"异常堆栈: {traceback.format_exc()}")
        return False


def test_data_fetch():
    """测试数据获取"""
    try:
        from instock.core.singleton_stock import stock_data
        from instock.core.stockfetch import fetch_etfs
        import datetime

        logging.info("开始测试数据获取...")

        # 获取当前日期
        today = datetime.datetime.now().date()
        logging.info(f"测试日期: {today}")

        # 测试股票数据获取
        logging.info("测试股票数据获取...")
        stock_data_obj = stock_data(today)
        data = stock_data_obj.get_data()

        if data is not None:
            logging.info(f"股票数据获取成功，行数: {len(data.index)}")
            logging.info(f"数据列: {list(data.columns)}")
            if len(data.index) > 0:
                logging.info(f"第一行数据: {data.iloc[0].to_dict()}")
        else:
            logging.warning("股票数据获取失败，返回None")

        # 测试ETF数据获取
        logging.info("测试ETF数据获取...")
        etf_data = fetch_etfs(today)

        if etf_data is not None:
            logging.info(f"ETF数据获取成功，行数: {len(etf_data.index)}")
            logging.info(f"数据列: {list(etf_data.columns)}")
            if len(etf_data.index) > 0:
                logging.info(f"第一行数据: {etf_data.iloc[0].to_dict()}")
        else:
            logging.warning("ETF数据获取失败，返回None")

        logging.info("数据获取测试完成!")
        return True

    except Exception as e:
        logging.error(f"数据获取测试失败: {e}")
        import traceback

        logging.error(f"异常堆栈: {traceback.format_exc()}")
        return False


def test_trade_date():
    """测试交易日期获取"""
    try:
        from instock.lib.trade_time import get_trade_date_last, is_trade_date
        import datetime

        logging.info("开始测试交易日期...")

        today = datetime.datetime.now().date()
        logging.info(f"当前日期: {today}")

        # 获取交易日期
        run_date, run_date_nph = get_trade_date_last()
        logging.info(f"交易日期 - run_date: {run_date}, run_date_nph: {run_date_nph}")

        # 检查是否为交易日
        is_today_trade = is_trade_date(today)
        logging.info(f"今天是否为交易日: {is_today_trade}")

        is_run_date_trade = is_trade_date(run_date)
        logging.info(f"run_date是否为交易日: {is_run_date_trade}")

        is_run_date_nph_trade = is_trade_date(run_date_nph)
        logging.info(f"run_date_nph是否为交易日: {is_run_date_nph_trade}")

        logging.info("交易日期测试完成!")
        return True

    except Exception as e:
        logging.error(f"交易日期测试失败: {e}")
        import traceback

        logging.error(f"异常堆栈: {traceback.format_exc()}")
        return False


def main():
    """主函数"""
    logging.info("=" * 50)
    logging.info("开始数据库诊断测试")
    logging.info("=" * 50)

    # 测试数据库连接
    db_ok = test_database_connection()

    # 测试数据获取
    data_ok = test_data_fetch()

    # 测试交易日期
    date_ok = test_trade_date()

    # 总结
    logging.info("=" * 50)
    logging.info("诊断测试总结:")
    logging.info(f"数据库连接: {'✓' if db_ok else '✗'}")
    logging.info(f"数据获取: {'✓' if data_ok else '✗'}")
    logging.info(f"交易日期: {'✓' if date_ok else '✗'}")

    if all([db_ok, data_ok, date_ok]):
        logging.info("所有测试通过，系统应该可以正常工作!")
    else:
        logging.warning("存在一些问题，请检查上述错误信息!")

    logging.info("=" * 50)


if __name__ == "__main__":
    main()
