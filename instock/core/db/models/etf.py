from sqlalchemy import Column, String, Integer, BIGINT, Float, Date
from .base import Base


class StockETFSpot(Base):
    """每日ETF数据"""

    __tablename__ = "cn_etf_spot"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    new_price = Column(Float, comment="最新价")
    change_rate = Column(Float, comment="涨跌幅")
    ups_downs = Column(Float, comment="涨跌额")
    volume = Column(Integer, comment="成交量")
    deal_amount = Column(BIGINT, comment="成交额")
    open_price = Column(Float, comment="开盘价")
    high_price = Column(Float, comment="最高价")
    low_price = Column(Float, comment="最低价")
    pre_close_price = Column(Float, comment="昨收")
    turnoverrate = Column(Float, comment="换手率")
    total_market_cap = Column(BIGINT, comment="总市值")
    free_cap = Column(BIGINT, comment="流通市值")
