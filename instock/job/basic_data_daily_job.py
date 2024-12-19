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
    if before:
        return
    # 股票列表
    try:
        data = stock_data(date).get_data()
        if data is None or len(data.index) == 0:
            return

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 删除当天数据
            db.query(StockSpot).filter(StockSpot.date == date).delete()

            # 将DataFrame转换为模型对象列表
            stock_objects = []
            for _, row in data.iterrows():
                # 将row中nan值替换为None
                row = {k: v if not pd.isna(v) else None for k, v in row.items()}
                stock = StockSpot(**row)
                stock_objects.append(stock)

            # 批量插入数据
            db.bulk_save_objects(stock_objects)
            db.commit()

    except Exception as e:
        logging.error(f"basic_data_daily_job.save_stock_spot_data处理异常：{e}")


# 基金实时行情数据。
def save_nph_etf_spot_data(date, before=True):
    if before:
        return
    # 股票列表
    try:
        data = stf.fetch_etfs(date)
        if data is None or len(data.index) == 0:
            return

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 删除当天数据
            db.query(StockETFSpot).filter(StockETFSpot.date == date).delete()

            # 构建ETF对象列表
            etf_objects = []
            for _, row in data.iterrows():
                # 将row中nan值替换为None
                row = {k: v if not pd.isna(v) else None for k, v in row.items()}
                etf = StockETFSpot(**row)
                etf_objects.append(etf)

            # 批量插入数据
            db.bulk_save_objects(etf_objects)
            db.commit()
    except Exception as e:
        logging.error(f"basic_data_daily_job.save_nph_etf_spot_data处理异常：{e}")


def main():
    runt.run_with_args(save_nph_stock_spot_data)
    runt.run_with_args(save_nph_etf_spot_data)


# main函数入口
if __name__ == "__main__":
    main()
