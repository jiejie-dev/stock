#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import os.path
import sys

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
from instock.core.db import DatabaseSession, StockBlockTrade
import instock.lib.run_template as runt
import instock.core.tablestructure as tbs
import instock.lib.database as mdb
import instock.core.stockfetch as stf

__author__ = "myh "
__date__ = "2023/3/10 "


# 每日股票大宗交易
def save_after_close_stock_blocktrade_data(date):
    try:
        data = stf.fetch_stock_blocktrade_data(date)
        if data is None or len(data.index) == 0:
            return

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 删除当天数据
            db.query(StockBlockTrade).filter(StockBlockTrade.date == date).delete()

            # 将DataFrame转换为模型对象列表
            blocktrade_objects = []
            for _, row in data.iterrows():
                blocktrade = StockBlockTrade(**row)
                blocktrade_objects.append(blocktrade)

            # 批量插入数据
            db.bulk_save_objects(blocktrade_objects)
            db.commit()
    except Exception as e:
        # 打印错误堆栈
        import traceback

        logging.error(traceback.format_exc())
        logging.error(
            f"basic_data_after_close_daily_job.save_stock_blocktrade_data处理异常：{e}"
        )


def main():
    runt.run_with_args(save_after_close_stock_blocktrade_data)


# main函数入口
if __name__ == "__main__":
    main()
