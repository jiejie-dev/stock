#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import logging
import pandas as pd
import numpy as np
import os.path
import sys

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
import instock.lib.run_template as runt
import instock.core.tablestructure as tbs
import instock.lib.database as mdb
import instock.core.stockfetch as stf

__author__ = "myh "
__date__ = "2023/5/5 "


def save_nph_stock_selection_data(date, before=True):
    if before:
        return

    try:
        data = stf.fetch_stock_selection()
        if data is None:
            return

        # 将NaN替换为None
        data = data.replace({np.nan: None})

        from instock.core.db import DatabaseSession, StockSelection

        # 删除老数据
        logging.info("######## 删除老数据：StockSelection #######")
        _date = data.iloc[0]["date"]
        with DatabaseSession() as db:
            db.query(StockSelection).filter(StockSelection.date == _date).delete()

            # 插入新数据
            records = []
            for _, row in data.iterrows():
                record = StockSelection(**row.to_dict())
                records.append(record)

            db.bulk_save_objects(records)
            db.commit()
    except Exception as e:
        logging.error(
            f"selection_data_daily_job.save_nph_stock_selection_data处理异常：{e}"
        )


def main():
    runt.run_with_args(save_nph_stock_selection_data)


# main函数入口
if __name__ == "__main__":
    main()
