from sqlalchemy import Column, String, Float, Date
from .base import Base


class StockBlockTrade(Base):
    """大宗交易"""

    __tablename__ = "cn_stock_blocktrade"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    new_price = Column(Float, comment="最新价")
    change_rate = Column(Float, comment="涨跌幅")
    average_price = Column(Float, comment="成交均价")
    overflow_rate = Column(Float, comment="折溢率")
    trade_number = Column(Float, comment="成交笔数")
    sum_volume = Column(Float, comment="成交总量")
    sum_turnover = Column(Float, comment="成交总额")
    turnover_market_rate = Column(Float, comment="成交占比流通市值")
