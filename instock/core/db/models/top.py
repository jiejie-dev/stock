from sqlalchemy import Column, DateTime, String, Float, Integer, Date
from .base import Base


class StockTop(Base):
    """龙虎榜"""

    __tablename__ = "cn_stock_top"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    new_price = Column(Float, comment="最新价")
    change_rate = Column(Float, comment="涨跌幅")
    volume = Column(Integer, comment="成交量")
    deal_amount = Column(Integer, comment="成交额")
    turnoverrate = Column(Float, comment="换手率")
    reason = Column(String(100), comment="上榜原因")
    buy_amount = Column(Integer, comment="买入金额")
    sell_amount = Column(Integer, comment="卖出金额")
    net_amount = Column(Integer, comment="净额")
    top_type = Column(String(20), comment="上榜类型")
    top_detail = Column(String(2000), comment="上榜明细")
    ranking_times = Column(Integer, comment="上榜次数")
    sum_buy = Column(Integer, comment="累积购买额")
    sum_sell = Column(Integer, comment="累积卖出额")
    buy_seat = Column(Integer, comment="买入席位数")
    sell_seat = Column(Integer, comment="卖出席位数")
    created_at = Column(DateTime, comment="创建时间")
