#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import concurrent.futures
import os.path
import sys
import pandas as pd

cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)
from instock.core.db import (
    DatabaseSession,
    StockBonus,
    StockFundFlow,
    StockFundFlowConcept,
    StockFundFlowIndustry,
    StockSpotBuy,
    StockTop,
)
import instock.lib.run_template as runt
import instock.core.tablestructure as tbs
import instock.lib.database as mdb
import instock.core.stockfetch as stf

__author__ = "myh "
__date__ = "2023/3/10 "


# 每日股票龙虎榜
def save_nph_stock_top_data(date, before=True):
    if before:
        return

    try:
        data = stf.fetch_stock_top_data(date)
        if data is None or len(data.index) == 0:
            return

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 删除当天数据
            db.query(StockTop).filter(StockTop.date == date).delete()

            # 将DataFrame转换为模型对象列表
            stock_objects = []
            for _, row in data.iterrows():
                stock = StockTop(
                    date=date,
                    code=row["code"],
                    name=row["name"],
                    rank=row["rank"],
                    reason=row["reason"],
                    buy_value=row["buy_value"],
                    sell_value=row["sell_value"],
                    net_value=row["net_value"],
                    buy_count=row["buy_count"],
                    sell_count=row["sell_count"],
                )
                stock_objects.append(stock)

            # 批量插入数据
            db.bulk_save_objects(stock_objects)
            db.commit()
    except Exception as e:
        logging.error(f"basic_data_other_daily_job.save_stock_top_data处理异常：{e}")
    stock_spot_buy(date)


# 每日股票资金流向
def save_nph_stock_fund_flow_data(date, before=True):
    if before:
        return

    try:
        times = tuple(range(4))
        results = run_check_stock_fund_flow(times)
        if results is None:
            return

        for t in times:
            if t == 0:
                data = results.get(t)
            else:
                r = results.get(t)
                if r is not None:
                    r.drop(columns=["name", "new_price"], inplace=True)
                    data = pd.merge(data, r, on=["code"], how="left")

        if data is None or len(data.index) == 0:
            return

        data.insert(0, "date", date.strftime("%Y-%m-%d"))

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 删除当天的老数据
            db.query(StockFundFlow).filter(StockFundFlow.date == date).delete()

            # 将DataFrame转换为模型对象列表
            fund_flow_objects = []
            for _, row in data.iterrows():
                fund_flow = StockFundFlow(
                    date=date,
                    code=row["code"],
                    name=row["name"],
                    new_price=row["new_price"],
                    change_rate=row["change_rate"],
                    fund_amount=row["fund_amount"],
                    fund_rate=row["fund_rate"],
                    fund_amount_super=row["fund_amount_super"],
                    fund_rate_super=row["fund_rate_super"],
                    fund_amount_large=row["fund_amount_large"],
                    fund_rate_large=row["fund_rate_large"],
                    fund_amount_medium=row["fund_amount_medium"],
                    fund_rate_medium=row["fund_rate_medium"],
                    fund_amount_small=row["fund_amount_small"],
                    fund_rate_small=row["fund_rate_small"],
                )
                fund_flow_objects.append(fund_flow)

            # 批量插入数据
            db.bulk_save_objects(fund_flow_objects)
            db.commit()
    except Exception as e:
        logging.error(
            f"basic_data_other_daily_job.save_nph_stock_fund_flow_data处理异常：{e}"
        )


def run_check_stock_fund_flow(times):
    data = {}
    try:
        for k in times:
            _data = stf.fetch_stocks_fund_flow(k)
            if _data is not None:
                data[k] = _data
    except Exception as e:
        logging.error(
            f"basic_data_other_daily_job.run_check_stock_fund_flow处理异常：{e}"
        )
    # try:
    #     with concurrent.futures.ThreadPoolExecutor(max_workers=len(times)) as executor:
    #         future_to_data = {executor.submit(stf.fetch_stocks_fund_flow, k): k for k in times}
    #         for future in concurrent.futures.as_completed(future_to_data):
    #             _time = future_to_data[future]
    #             try:
    #                 _data_ = future.result()
    #                 if _data_ is not None:
    #                     data[_time] = _data_
    #             except Exception as e:
    #                 logging.error(f"basic_data_other_daily_job.run_check_stock_fund_flow处理异常：代码{e}")
    # except Exception as e:
    #     logging.error(f"basic_data_other_daily_job.run_check_stock_fund_flow处理异常：{e}")
    if not data:
        return None
    else:
        return data


# 每日行业资金流向
def save_nph_stock_sector_fund_flow_data(date, before=True):
    if before:
        return

    # times = tuple(range(2))
    # with concurrent.futures.ThreadPoolExecutor(max_workers=len(times)) as executor:
    #     {executor.submit(stock_sector_fund_flow_data, date, k): k for k in times}
    stock_sector_fund_flow_data(date, 0)
    stock_sector_fund_flow_data(date, 1)


def stock_sector_fund_flow_data(date, index_sector):
    try:
        times = tuple(range(3))
        results = run_check_stock_sector_fund_flow(index_sector, times)
        if results is None:
            return

        for t in times:
            if t == 0:
                data = results.get(t)
            else:
                r = results.get(t)
                if r is not None:
                    data = pd.merge(data, r, on=["name"], how="left")

        if data is None or len(data.index) == 0:
            return

        data.insert(0, "date", date.strftime("%Y-%m-%d"))

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 根据行业/概念选择对应的模型类
            if index_sector == 0:
                model_class = StockFundFlowIndustry
            else:
                model_class = StockFundFlowConcept

            # 删除当天的老数据
            db.query(model_class).filter(model_class.date == date).delete()

            # 将DataFrame转换为模型对象列表并批量插入
            records = []
            for _, row in data.iterrows():
                record = model_class()
                for column in data.columns:
                    setattr(record, column, row[column])
                records.append(record)

            db.bulk_save_objects(records)
            db.commit()
    except Exception as e:
        logging.error(
            f"basic_data_other_daily_job.stock_sector_fund_flow_data处理异常：{e}"
        )


def run_check_stock_sector_fund_flow(index_sector, times):
    data = {}
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(times)) as executor:
            future_to_data = {
                executor.submit(stf.fetch_stocks_sector_fund_flow, index_sector, k): k
                for k in times
            }
            for future in concurrent.futures.as_completed(future_to_data):
                _time = future_to_data[future]
                try:
                    _data_ = future.result()
                    if _data_ is not None:
                        data[_time] = _data_
                except Exception as e:
                    logging.error(
                        f"basic_data_other_daily_job.run_check_stock_sector_fund_flow处理异常：代码{e}"
                    )
    except Exception as e:
        logging.error(
            f"basic_data_other_daily_job.run_check_stock_sector_fund_flow处理异常：{e}"
        )
    if not data:
        return None
    else:
        return data


# 每日股票分红配送
def save_nph_stock_bonus(date, before=True):
    if before:
        return

    try:
        data = stf.fetch_stocks_bonus(date)
        if data is None or len(data.index) == 0:
            return

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 删除当天的老数据
            db.query(StockBonus).filter(StockBonus.date == date).delete()

            # 将DataFrame转换为模型对象列表
            bonus_objects = []
            for _, row in data.iterrows():
                bonus = StockBonus(
                    date=date,
                    code=row["code"],
                    name=row["name"],
                    convertible_total_rate=row["convertible_total_rate"],
                    convertible_rate=row["convertible_rate"],
                    convertible_transfer_rate=row["convertible_transfer_rate"],
                    bonusaward_rate=row["bonusaward_rate"],
                    bonusaward_yield=row["bonusaward_yield"],
                    basic_eps=row["basic_eps"],
                    bvps=row["bvps"],
                    per_capital_reserve=row["per_capital_reserve"],
                    per_unassign_profit=row["per_unassign_profit"],
                    netprofit_yoy_ratio=row["netprofit_yoy_ratio"],
                    total_shares=row["total_shares"],
                    plan_date=row["plan_date"],
                    record_date=row["record_date"],
                    ex_dividend_date=row["ex_dividend_date"],
                    progress=row["progress"],
                    report_date=row["report_date"],
                )
                bonus_objects.append(bonus)

            # 批量插入数据
            db.bulk_save_objects(bonus_objects)
            db.commit()
    except Exception as e:
        logging.error(f"basic_data_other_daily_job.save_nph_stock_bonus处理异常：{e}")


# 基本面选股
def stock_spot_buy(date):
    try:
        _table_name = tbs.TABLE_CN_STOCK_SPOT["name"]
        if not mdb.checkTableIsExist(_table_name):
            return

        sql = f"""SELECT * FROM `{_table_name}` WHERE `date` = '{date}' and 
                `pe9` > 0 and `pe9` <= 20 and `pbnewmrq` <= 10 and `roe_weight` >= 15"""
        data = pd.read_sql(sql=sql, con=mdb.engine())
        data = data.drop_duplicates(subset="code", keep="last")
        if len(data.index) == 0:
            return

        # 使用上下文管理器处理数据库会话
        with DatabaseSession() as db:
            # 删除当天数据
            db.query(StockSpotBuy).filter(StockSpotBuy.date == date).delete()

            # 将DataFrame转换为模型对象列表
            spot_buy_objects = []
            for _, row in data.iterrows():
                spot_buy = StockSpotBuy(
                    date=date,
                    code=row["code"],
                    name=row["name"],
                    pe9=row["pe9"],
                    pbnewmrq=row["pbnewmrq"],
                    roe_weight=row["roe_weight"],
                )
                spot_buy_objects.append(spot_buy)

            # 批量插入数据
            db.bulk_save_objects(spot_buy_objects)
            db.commit()
    except Exception as e:
        logging.error(f"basic_data_other_daily_job.stock_spot_buy处理异常：{e}")


def main():
    runt.run_with_args(save_nph_stock_top_data)
    runt.run_with_args(save_nph_stock_bonus)
    runt.run_with_args(save_nph_stock_fund_flow_data)
    runt.run_with_args(save_nph_stock_sector_fund_flow_data)


# main函数入口
if __name__ == "__main__":
    main()
