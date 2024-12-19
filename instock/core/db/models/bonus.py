from sqlalchemy import BIGINT, Column, DateTime, String, Float, Date, Integer
from .base import Base


class StockBonus(Base):
    """股票分红"""

    __tablename__ = "cn_stock_bonus"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    convertible_total_rate = Column(Float, comment="送转总比例")
    convertible_rate = Column(Float, comment="送股比例")
    convertible_transfer_rate = Column(Float, comment="转股比例")
    bonusaward_rate = Column(Float, comment="派息比例")
    bonusaward_yield = Column(Float, comment="股息率")
    basic_eps = Column(Float, comment="每股收益")
    bvps = Column(Float, comment="每股净资产")
    per_capital_reserve = Column(Float, comment="每股公积金")
    per_unassign_profit = Column(Float, comment="每股未分配利润")
    netprofit_yoy_ratio = Column(Float, comment="净利润同比增长率")
    total_shares = Column(BIGINT, comment="总股本")
    plan_date = Column(Date, comment="预案公告日")
    record_date = Column(Date, comment="股权登记日")
    ex_dividend_date = Column(Date, comment="除权除息日")
    progress = Column(String(20), comment="方案进度")
    report_date = Column(Date, comment="报告期")
    created_at = Column(DateTime, comment="创建时间")
