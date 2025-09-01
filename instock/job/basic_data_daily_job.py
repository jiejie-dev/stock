#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import os.path
import sys

import pandas as pd

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
import instock.lib.run_template as runt
import instock.core.stockfetch as stf
from instock.core.singleton_stock import stock_data
from instock.core.db import DatabaseSession, StockSpot, StockETFSpot

__author__ = "myh "
__date__ = "2023/3/10 "


# 股票实时行情数据。
def save_nph_stock_spot_data(date, before=True):
    logging.info(f"开始执行股票数据插入，日期: {date}, before: {before}")

    if before:
        logging.info(f"before=True，跳过股票数据插入，日期: {date}")
        return

    # 股票列表
    try:
        logging.info(f"开始获取股票数据，日期: {date}")
        data = stock_data(date).get_data()

        if data is None:
            logging.warning(f"股票数据为None，日期: {date}")
            return

        if len(data.index) == 0:
            logging.warning(f"股票数据为空DataFrame，日期: {date}")
            return

        logging.info(f"成功获取股票数据，行数: {len(data.index)}, 日期: {date}")
        logging.info(f"数据列: {list(data.columns)}")
        logging.info(f"前5行数据预览: {data.head().to_dict()}")

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 删除当天数据
            delete_count = db.query(StockSpot).filter(StockSpot.date == date).delete()
            logging.info(f"删除原有数据，删除行数: {delete_count}, 日期: {date}")
            db.commit()

            # 将DataFrame转换为模型对象列表
            stock_objects = []
            for _, row in data.iterrows():
                # 将row中nan值替换为None
                row = {k: v if not pd.isna(v) else None for k, v in row.items()}
                stock = StockSpot(**row)
                stock_objects.append(stock)

            logging.info(
                f"准备插入股票数据，对象数量: {len(stock_objects)}, 日期: {date}"
            )

            # 批量插入数据
            db.bulk_save_objects(stock_objects)
            db.commit()

            logging.info(
                f"股票数据插入成功，插入行数: {len(stock_objects)}, 日期: {date}"
            )

    except Exception as e:
        logging.error(f"basic_data_daily_job.save_stock_spot_data处理异常：{e}")
        logging.error(f"异常详情：{str(e)}")
        import traceback

        logging.error(f"异常堆栈：{traceback.format_exc()}")


# 基金实时行情数据。
def save_nph_etf_spot_data(date, before=True):
    logging.info(f"开始执行ETF数据插入，日期: {date}, before: {before}")

    if before:
        logging.info(f"before=True，跳过ETF数据插入，日期: {date}")
        return

    # 股票列表
    try:
        logging.info(f"开始获取ETF数据，日期: {date}")
        data = stf.fetch_etfs(date)

        if data is None:
            logging.warning(f"ETF数据为None，日期: {date}")
            return

        if len(data.index) == 0:
            logging.warning(f"ETF数据为空DataFrame，日期: {date}")
            return

        logging.info(f"成功获取ETF数据，行数: {len(data.index)}, 日期: {date}")
        logging.info(f"数据列: {list(data.columns)}")
        logging.info(f"前5行数据预览: {data.head().to_dict()}")

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 删除当天数据
            delete_count = (
                db.query(StockETFSpot).filter(StockETFSpot.date == date).delete()
            )
            logging.info(f"删除原有ETF数据，删除行数: {delete_count}, 日期: {date}")
            db.commit()

            # 构建ETF对象列表
            etf_objects = []
            for _, row in data.iterrows():
                # 将row中nan值替换为None
                row = {k: v if not pd.isna(v) else None for k, v in row.items()}
                etf = StockETFSpot(**row)
                etf_objects.append(etf)

            logging.info(f"准备插入ETF数据，对象数量: {len(etf_objects)}, 日期: {date}")

            # 批量插入数据
            db.bulk_save_objects(etf_objects)
            db.commit()

            logging.info(f"ETF数据插入成功，插入行数: {len(etf_objects)}, 日期: {date}")

    except Exception as e:
        logging.error(f"basic_data_daily_job.save_nph_etf_spot_data处理异常：{e}")
        logging.error(f"异常详情：{str(e)}")
        import traceback

        logging.error(f"异常堆栈：{traceback.format_exc()}")


def main():
    logging.info("开始执行基础数据每日任务")
    runt.run_with_args(save_nph_stock_spot_data)
    runt.run_with_args(save_nph_etf_spot_data)
    logging.info("基础数据每日任务执行完成")


# main函数入口
if __name__ == "__main__":
    main()
