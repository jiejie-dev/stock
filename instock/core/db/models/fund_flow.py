from sqlalchemy import Column, String, Integer, BIGINT, Float, Date, DateTime
from .base import Base


class StockFundFlow(Base):
    """股票资金流"""

    __tablename__ = "cn_stock_fund_flow"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    new_price = Column(Float, comment="最新价")

    # 涨跌幅
    change_rate = Column(Float, comment="涨跌幅")
    change_rate_3 = Column(Float, comment="3日涨跌幅")
    change_rate_5 = Column(Float, comment="5日涨跌幅")
    change_rate_10 = Column(Float, comment="10日涨跌幅")
    change_rate_20 = Column(Float, comment="20日涨跌幅")

    # 主力资金
    fund_amount = Column(BIGINT, comment="主力净流入-净额")
    fund_rate = Column(Float, comment="主力净流入-净占比")

    # 超大单资金
    fund_amount_super = Column(BIGINT, comment="超大单净流入-净额")
    fund_rate_super = Column(Float, comment="超大单净流入-净占比")

    # 大单资金
    fund_amount_large = Column(BIGINT, comment="大单净流入-净额")
    fund_rate_large = Column(Float, comment="大单净流入-净占比")

    # 中单资金
    fund_amount_medium = Column(BIGINT, comment="中单净流入-净额")
    fund_rate_medium = Column(Float, comment="中单净流入-净占比")

    # 小单资金
    fund_amount_small = Column(BIGINT, comment="小单净流入-净额")
    fund_rate_small = Column(Float, comment="小单净流入-净占比")

    # 3日资金
    fund_amount_3days = Column(BIGINT, comment="3日主力净额")
    fund_rate_3days = Column(Float, comment="3日主力净占比")
    fund_amount_3 = Column(BIGINT, comment="3日主力净额")
    fund_rate_3 = Column(Float, comment="3日主力净占比")
    fund_amount_super_3 = Column(BIGINT, comment="3日超大单净额")
    fund_rate_super_3 = Column(Float, comment="3日超大单净占比")
    fund_amount_large_3 = Column(BIGINT, comment="3日大单净额")
    fund_rate_large_3 = Column(Float, comment="3日大单净占比")
    fund_amount_medium_3 = Column(BIGINT, comment="3日中单净额")
    fund_rate_medium_3 = Column(Float, comment="3日中单净占比")
    fund_amount_small_3 = Column(BIGINT, comment="3日小单净额")
    fund_rate_small_3 = Column(Float, comment="3日小单净占比")

    # 5日资金
    fund_amount_5days = Column(BIGINT, comment="5日主力净额")
    fund_rate_5days = Column(Float, comment="5日主力净占比")
    fund_amount_5 = Column(BIGINT, comment="5日主力净额")
    fund_rate_5 = Column(Float, comment="5日主力净占比")
    fund_amount_super_5 = Column(BIGINT, comment="5日超大单净额")
    fund_rate_super_5 = Column(Float, comment="5日超大单净占比")
    fund_amount_large_5 = Column(BIGINT, comment="5日大单净额")
    fund_rate_large_5 = Column(Float, comment="5日大单净占比")
    fund_amount_medium_5 = Column(BIGINT, comment="5日中单净额")
    fund_rate_medium_5 = Column(Float, comment="5日中单净占比")
    fund_amount_small_5 = Column(BIGINT, comment="5日小单净额")
    fund_rate_small_5 = Column(Float, comment="5日小单净占比")

    # 10日资金
    fund_amount_10days = Column(BIGINT, comment="10日主力净额")
    fund_rate_10days = Column(Float, comment="10日主力净占比")
    fund_amount_10 = Column(BIGINT, comment="10日主力净额")
    fund_rate_10 = Column(Float, comment="10日主力净占比")
    fund_amount_super_10 = Column(BIGINT, comment="10日超大单净额")
    fund_rate_super_10 = Column(Float, comment="10日超大单净占比")
    fund_amount_large_10 = Column(BIGINT, comment="10日大单净额")
    fund_rate_large_10 = Column(Float, comment="10日大单净占比")
    fund_amount_medium_10 = Column(BIGINT, comment="10日中单净额")
    fund_rate_medium_10 = Column(Float, comment="10日中单净占比")
    fund_amount_small_10 = Column(BIGINT, comment="10日小单净额")
    fund_rate_small_10 = Column(Float, comment="10日小单净占比")


class StockFundFlowConcept(Base):
    """概念资金流向"""

    __tablename__ = "cn_stock_fund_flow_concept"

    date = Column(Date, primary_key=True, comment="日期")
    name = Column(String(50), primary_key=True, comment="概念名称")
    concept = Column(String(50), comment="概念名称")
    stock_name = Column(String(20), comment="股票名称")

    # 涨跌幅
    change_rate = Column(Float, comment="涨跌幅")
    change_rate_3 = Column(Float, comment="3日涨跌幅")
    change_rate_5 = Column(Float, comment="5日涨跌幅")
    change_rate_10 = Column(Float, comment="10日涨跌幅")
    change_rate_20 = Column(Float, comment="20日涨跌幅")

    # 主力资金
    fund_amount = Column(BIGINT, comment="主力净流入-净额")
    fund_rate = Column(Float, comment="主力净流入-净占比")

    # 超大单资金
    fund_amount_super = Column(BIGINT, comment="超大单净流入-净额")
    fund_rate_super = Column(Float, comment="超大单净流入-净占比")

    # 大单资金
    fund_amount_large = Column(BIGINT, comment="大单净流入-净额")
    fund_rate_large = Column(Float, comment="大单净流入-净占比")

    # 中���资金
    fund_amount_medium = Column(BIGINT, comment="中单净流入-净额")
    fund_rate_medium = Column(Float, comment="中单净流入-净占比")

    # 小单资金
    fund_amount_small = Column(BIGINT, comment="小单净流入-净额")
    fund_rate_small = Column(Float, comment="小单净流入-净占比")

    # 3日资金
    fund_amount_3days = Column(BIGINT, comment="3日主力净额")
    fund_rate_3days = Column(Float, comment="3日主力净占比")
    fund_amount_3 = Column(BIGINT, comment="3日主力净额")
    fund_rate_3 = Column(Float, comment="3日主力净占比")
    fund_amount_super_3 = Column(BIGINT, comment="3日超大单净额")
    fund_rate_super_3 = Column(Float, comment="3日超大单净占比")
    fund_amount_large_3 = Column(BIGINT, comment="3日大单净额")
    fund_rate_large_3 = Column(Float, comment="3日大单净占比")
    fund_amount_medium_3 = Column(BIGINT, comment="3日中单净额")
    fund_rate_medium_3 = Column(Float, comment="3日中单净占比")
    fund_amount_small_3 = Column(BIGINT, comment="3日小单净额")
    fund_rate_small_3 = Column(Float, comment="3日小单净占比")

    # 5日资金
    fund_amount_5days = Column(BIGINT, comment="5日主力净额")
    fund_rate_5days = Column(Float, comment="5日主力净占比")
    fund_amount_5 = Column(BIGINT, comment="5日主力净额")
    fund_rate_5 = Column(Float, comment="5日主力净占比")
    fund_amount_super_5 = Column(BIGINT, comment="5日超大单净额")
    fund_rate_super_5 = Column(Float, comment="5日超大单净占比")
    fund_amount_large_5 = Column(BIGINT, comment="5日大单净额")
    fund_rate_large_5 = Column(Float, comment="5日大单净占比")
    fund_amount_medium_5 = Column(BIGINT, comment="5日中单净额")
    fund_rate_medium_5 = Column(Float, comment="5日中单净占比")
    fund_amount_small_5 = Column(BIGINT, comment="5日小单净额")
    fund_rate_small_5 = Column(Float, comment="5日小单净占比")

    # 10日资金
    fund_amount_10days = Column(BIGINT, comment="10日主力净额")
    fund_rate_10days = Column(Float, comment="10日主力净占比")
    fund_amount_10 = Column(BIGINT, comment="10日主力净额")
    fund_rate_10 = Column(Float, comment="10日主力净占比")
    fund_amount_super_10 = Column(BIGINT, comment="10日超大单净额")
    fund_rate_super_10 = Column(Float, comment="10日超大单净占比")
    fund_amount_large_10 = Column(BIGINT, comment="10日大单净额")
    fund_rate_large_10 = Column(Float, comment="10日大单净占比")
    fund_amount_medium_10 = Column(BIGINT, comment="10日中单净额")
    fund_rate_medium_10 = Column(Float, comment="10日中单净占比")
    fund_amount_small_10 = Column(BIGINT, comment="10日小单净额")
    fund_rate_small_10 = Column(Float, comment="10日小单净占比")

    # 统计数据
    stock_count = Column(Integer, comment="股票数量")
    rise_count = Column(Integer, comment="上涨家数")
    fall_count = Column(Integer, comment="下跌家数")

    # 涨跌幅
    rise_max = Column(Float, comment="涨跌幅最大")
    fall_max = Column(Float, comment="涨跌幅最小")

    created_at = Column(DateTime, comment="创建时间")

    # 3日领涨股
    stock_name_3 = Column(String(20), comment="3日领涨股")
    stock_code_3 = Column(String(6), comment="3日领涨股代码")
    stock_rate_3 = Column(Float, comment="3日领涨股涨跌幅")

    # 5日领涨股
    stock_name_5 = Column(String(20), comment="5日领涨股")
    stock_code_5 = Column(String(6), comment="5日领涨股代码")
    stock_rate_5 = Column(Float, comment="5日领涨股涨跌幅")

    # 10日领涨股
    stock_name_10 = Column(String(20), comment="10日领涨股")
    stock_code_10 = Column(String(6), comment="10日领涨股代码")
    stock_rate_10 = Column(Float, comment="10日领涨股涨��幅")

    # 20日领涨股
    stock_name_20 = Column(String(20), comment="20日领涨股")
    stock_code_20 = Column(String(6), comment="20日领涨股代码")
    stock_rate_20 = Column(Float, comment="20日领涨股涨跌幅")


class StockFundFlowIndustry(Base):
    """行业资金流向"""

    __tablename__ = "cn_stock_fund_flow_industry"

    date = Column(Date, primary_key=True, comment="日期")
    name = Column(String(20), primary_key=True, comment="行业名称")
    industry = Column(String(20), comment="行业名称")
    stock_name = Column(String(20), comment="股票名称")

    # 涨跌幅
    change_rate = Column(Float, comment="涨跌幅")
    change_rate_3 = Column(Float, comment="3日涨跌幅")
    change_rate_5 = Column(Float, comment="5日涨跌幅")
    change_rate_10 = Column(Float, comment="10日涨跌幅")
    change_rate_20 = Column(Float, comment="20日涨跌幅")

    # 主力资金
    fund_amount = Column(BIGINT, comment="主力净流入-净额")
    fund_rate = Column(Float, comment="主力净流入-净占比")

    # 超大单资金
    fund_amount_super = Column(BIGINT, comment="超大单净流入-净额")
    fund_rate_super = Column(Float, comment="超大单净流入-净占比")

    # 大单资金
    fund_amount_large = Column(BIGINT, comment="大单净流入-净额")
    fund_rate_large = Column(Float, comment="大单净流入-净占比")

    # 中单资金
    fund_amount_medium = Column(BIGINT, comment="中单净流入-净额")
    fund_rate_medium = Column(Float, comment="中单净流入-净占比")

    # 小单资金
    fund_amount_small = Column(BIGINT, comment="小单净流入-净额")
    fund_rate_small = Column(Float, comment="小单净流入-净占比")

    # 3日资金
    fund_amount_3days = Column(BIGINT, comment="3日主力净额")
    fund_rate_3days = Column(Float, comment="3日主力净占比")
    fund_amount_3 = Column(BIGINT, comment="3日主力净额")
    fund_rate_3 = Column(Float, comment="3日主力净占比")
    fund_amount_super_3 = Column(BIGINT, comment="3日超大单净额")
    fund_rate_super_3 = Column(Float, comment="3日超大单净占比")
    fund_amount_large_3 = Column(BIGINT, comment="3日大单净额")
    fund_rate_large_3 = Column(Float, comment="3日大单净占比")
    fund_amount_medium_3 = Column(BIGINT, comment="3日中单净额")
    fund_rate_medium_3 = Column(Float, comment="3日中单净占比")
    fund_amount_small_3 = Column(BIGINT, comment="3日小单净额")
    fund_rate_small_3 = Column(Float, comment="3日小单净占比")

    # 5日资金
    fund_amount_5days = Column(BIGINT, comment="5日主力净额")
    fund_rate_5days = Column(Float, comment="5日主力净占比")
    fund_amount_5 = Column(BIGINT, comment="5日主力净额")
    fund_rate_5 = Column(Float, comment="5日主力净占比")
    fund_amount_super_5 = Column(BIGINT, comment="5日超大单净额")
    fund_rate_super_5 = Column(Float, comment="5日超大单净占比")
    fund_amount_large_5 = Column(BIGINT, comment="5日大单净额")
    fund_rate_large_5 = Column(Float, comment="5日大单净占比")
    fund_amount_medium_5 = Column(BIGINT, comment="5日中单净额")
    fund_rate_medium_5 = Column(Float, comment="5日中单净占比")
    fund_amount_small_5 = Column(BIGINT, comment="5日小单净额")
    fund_rate_small_5 = Column(Float, comment="5日小单净占比")

    # 10日资金
    fund_amount_10days = Column(BIGINT, comment="10日主力净额")
    fund_rate_10days = Column(Float, comment="10日主力净占比")
    fund_amount_10 = Column(BIGINT, comment="10日主力净额")
    fund_rate_10 = Column(Float, comment="10日主力净占比")
    fund_amount_super_10 = Column(BIGINT, comment="10日超大单净额")
    fund_rate_super_10 = Column(Float, comment="10日超大单净占比")
    fund_amount_large_10 = Column(BIGINT, comment="10日大单净额")
    fund_rate_large_10 = Column(Float, comment="10日大单净占比")
    fund_amount_medium_10 = Column(BIGINT, comment="10日中单净额")
    fund_rate_medium_10 = Column(Float, comment="10日中单净占比")
    fund_amount_small_10 = Column(BIGINT, comment="10日小单净额")
    fund_rate_small_10 = Column(Float, comment="10日小单净占比")

    # 统计数据
    stock_count = Column(Integer, comment="股票数量")
    rise_count = Column(Integer, comment="上涨家数")
    fall_count = Column(Integer, comment="下跌家数")

    # 涨跌幅
    rise_max = Column(Float, comment="涨跌幅最大")
    fall_max = Column(Float, comment="涨跌幅最小")

    created_at = Column(DateTime, comment="创建时间")

    # 3日领涨股
    stock_name_3 = Column(String(20), comment="3日领涨股")
    stock_code_3 = Column(String(6), comment="3日领涨股代码")
    stock_rate_3 = Column(Float, comment="3日领涨股涨跌幅")

    # 5日领涨股
    stock_name_5 = Column(String(20), comment="5日领涨股")
    stock_code_5 = Column(String(6), comment="5日领涨股代码")
    stock_rate_5 = Column(Float, comment="5日领涨股涨跌幅")

    # 10日领涨股
    stock_name_10 = Column(String(20), comment="10日领涨股")
    stock_code_10 = Column(String(6), comment="10日领涨股代码")
    stock_rate_10 = Column(Float, comment="10日领涨股涨跌幅")

    # 20日领涨股
    stock_name_20 = Column(String(20), comment="20日领涨股")
    stock_code_20 = Column(String(6), comment="20日领涨股代码")
    stock_rate_20 = Column(Float, comment="20日领涨股涨跌幅")
