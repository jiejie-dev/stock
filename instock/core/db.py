from sqlalchemy import (
    BIGINT,
    Column,
    Integer,
    String,
    Date,
    Float,
    DateTime,
    SmallInteger,
    create_engine,
)
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
import os
import logging


# 使用新的方式创建 Base
class Base(DeclarativeBase):
    pass


# 数据库连接配置
db_host = os.environ.get("db_host", "localhost")
db_user = os.environ.get("db_user", "root")
db_password = os.environ.get("db_password", "root")
db_database = os.environ.get("db_database", "instockdb")
db_port = int(os.environ.get("db_port", "3306"))
db_charset = "utf8mb4"

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}?charset={db_charset}"

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    pool_size=20,  # 连接池大小
    max_overflow=10,  # 超过pool_size后最多可以创建的连接数
    pool_timeout=30,  # 池中没有连接时等待的秒数
    pool_recycle=3600,  # 连接重置周期(秒)
    echo=False,  # 是否打印SQL语句
)

# 创建会话工厂
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 创建线程安全的会话工厂
session_factory = scoped_session(SessionLocal)


def init_db():
    """初始化数据库"""
    try:
        # 创建所有表
        Base.metadata.create_all(engine)
        logging.info("数据库表创建成功")
    except Exception as e:
        logging.error(f"数据库表创建失败: {str(e)}")
        raise


def get_db():
    """获取数据库会话"""
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def get_engine():
    """获取数据库引擎"""
    return engine


# 数据库会话上下文管理器
class DatabaseSession:
    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = session_factory()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # 发生异常,回滚
            self.db.rollback()
            logging.error(f"数据库操作异常: {str(exc_val)}")
        self.db.close()


# 使用示例:
"""
# 方式1: 使用上下文管理器
with DatabaseSession() as db:
    stock = db.query(StockSpot).filter_by(code='000001').first()
    
# 方式2: 使用生成器
db = next(get_db())
try:
    stock = db.query(StockSpot).filter_by(code='000001').first()
finally:
    db.close()
"""


class StockAttention(Base):
    """我的关注"""

    __tablename__ = "cn_stock_attention"

    datetime = Column(DateTime, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    created_at = Column(DateTime, comment="创建时间")


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


class StockSpot(Base):
    """每日股票数据"""

    __tablename__ = "cn_stock_spot"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    new_price = Column(Float, comment="最新价")
    change_rate = Column(Float, comment="涨跌幅")
    ups_downs = Column(Float, comment="涨跌额")
    volume = Column(Integer, comment="成交量")
    deal_amount = Column(BIGINT, comment="成交额")
    amplitude = Column(Float, comment="振幅")
    turnoverrate = Column(Float, comment="换手率")
    volume_ratio = Column(Float, comment="量比")
    open_price = Column(Float, comment="今开")
    high_price = Column(Float, comment="最高")
    low_price = Column(Float, comment="最低")
    pre_close_price = Column(Float, comment="昨收")
    speed_increase = Column(Float, comment="涨速")
    speed_increase_5 = Column(Float, comment="5分钟涨跌")
    speed_increase_60 = Column(Float, comment="60日涨跌幅")
    speed_increase_all = Column(Float, comment="年初至今涨跌幅")
    dtsyl = Column(Float, comment="市盈率动")
    pe9 = Column(Float, comment="市盈率TTM")
    pe = Column(Float, comment="市盈率")
    pbnewmrq = Column(Float, comment="市净率")
    basic_eps = Column(Float, comment="每股收益")
    bvps = Column(Float, comment="每股净资产")
    per_capital_reserve = Column(Float, comment="每股公积金")
    per_unassign_profit = Column(Float, comment="每股未分配利润")
    roe_weight = Column(Float, comment="加权净资产收益率")
    sale_gpr = Column(Float, comment="毛利率")
    debt_asset_ratio = Column(Float, comment="资产负债率")
    total_operate_income = Column(BIGINT, comment="营业收入")
    toi_yoy_ratio = Column(Float, comment="营业收入同比增长")
    parent_netprofit = Column(BIGINT, comment="归属净利润")
    netprofit_yoy_ratio = Column(Float, comment="归属净利润同比增长")
    report_date = Column(Date, comment="报告期")
    total_shares = Column(BIGINT, comment="总股本")
    free_shares = Column(BIGINT, comment="已流通股份")
    total_market_cap = Column(BIGINT, comment="总市值")
    free_cap = Column(BIGINT, comment="流通市值")
    industry = Column(String(20), comment="所处行业")
    listing_date = Column(Date, comment="上市时间")


class StockSpotBuy(Base):
    """基本面选股"""

    __tablename__ = "cn_stock_spot_buy"

    # 完整继承 StockSpot 的所有字段
    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    new_price = Column(Float, comment="最新价")
    change_rate = Column(Float, comment="涨跌幅")
    ups_downs = Column(Float, comment="涨跌额")
    volume = Column(Integer, comment="成交量")
    deal_amount = Column(BIGINT, comment="成交额")
    amplitude = Column(Float, comment="振幅")
    turnoverrate = Column(Float, comment="换手率")
    volume_ratio = Column(Float, comment="量比")
    open_price = Column(Float, comment="今开")
    high_price = Column(Float, comment="最高")
    low_price = Column(Float, comment="最低")
    pre_close_price = Column(Float, comment="昨收")
    speed_increase = Column(Float, comment="涨速")
    speed_increase_5 = Column(Float, comment="5分钟涨跌")
    speed_increase_60 = Column(Float, comment="60日涨跌幅")
    speed_increase_all = Column(Float, comment="年初至今涨跌幅")
    dtsyl = Column(Float, comment="市盈率动")
    pe9 = Column(Float, comment="市盈率TTM")
    pe = Column(Float, comment="市盈率静")
    pbnewmrq = Column(Float, comment="市净率")
    basic_eps = Column(Float, comment="每股收益")
    bvps = Column(Float, comment="每股净资产")
    per_capital_reserve = Column(Float, comment="每股公积金")
    per_unassign_profit = Column(Float, comment="每股未分配利润")
    roe_weight = Column(Float, comment="加权净资产收益率")
    sale_gpr = Column(Float, comment="毛利率")
    debt_asset_ratio = Column(Float, comment="资产负债率")
    total_operate_income = Column(BIGINT, comment="营业收入")
    toi_yoy_ratio = Column(Float, comment="营业收入同比增长")
    parent_netprofit = Column(BIGINT, comment="归属净利润")
    netprofit_yoy_ratio = Column(Float, comment="归属净利润同比增长")
    report_date = Column(Date, comment="报告期")
    total_shares = Column(BIGINT, comment="总股本")
    free_shares = Column(BIGINT, comment="已流通股份")
    total_market_cap = Column(BIGINT, comment="总市值")
    free_cap = Column(BIGINT, comment="流通市值")
    industry = Column(String(20), comment="所处行业")
    listing_date = Column(Date, comment="上市时间")


class StockFundFlow(Base):
    """股票资金流"""

    __tablename__ = "cn_stock_fund_flow"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    new_price = Column(Float, comment="最新价")
    change_rate = Column(Float, comment="今日涨跌幅")
    fund_amount = Column(Integer, comment="今日主力净流入-净额")
    fund_rate = Column(Float, comment="今日主力净流入-净占比")
    fund_amount_super = Column(Integer, comment="今日超大单净流入-净额")
    fund_rate_super = Column(Float, comment="今日超大单净流入-净占比")
    fund_amount_large = Column(Integer, comment="今日大单净流入-净额")
    fund_rate_large = Column(Float, comment="今日大单净流入-净占比")
    fund_amount_medium = Column(Integer, comment="今日中单净流入-净额")
    fund_rate_medium = Column(Float, comment="今日中单净流入-净占比")
    fund_amount_small = Column(Integer, comment="今日小单净流入-净额")
    fund_rate_small = Column(Float, comment="今日小单净流入-净占比")
    created_at = Column(DateTime, comment="创建时间")


class StockBonus(Base):
    """股票分红配送"""

    __tablename__ = "cn_stock_bonus"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    convertible_total_rate = Column(Float, comment="送转股份-送转总比例")
    convertible_rate = Column(Float, comment="送转股份-送转比例")
    convertible_transfer_rate = Column(Float, comment="送转股份-转股比例")
    bonusaward_rate = Column(Float, comment="现金分红-现金分红比例")
    bonusaward_yield = Column(Float, comment="现金分红-股息率")
    basic_eps = Column(Float, comment="每股收益")
    bvps = Column(Float, comment="每股净资产")
    per_capital_reserve = Column(Float, comment="每股公积金")
    per_unassign_profit = Column(Float, comment="每股未分配利润")
    netprofit_yoy_ratio = Column(Float, comment="净利润同比增长")
    total_shares = Column(Integer, comment="总股本")
    plan_date = Column(Date, comment="预案公告日")
    record_date = Column(Date, comment="股权登记日")
    ex_dividend_date = Column(Date, comment="除权除息日")
    progress = Column(String(50), comment="方案进度")
    report_date = Column(Date, comment="最新公告日期")
    created_at = Column(DateTime, comment="创建时间")


class StockSelection(Base):
    """综合选股"""

    __tablename__ = "cn_stock_selection"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    new_price = Column(Float, comment="最新价")
    change_rate = Column(Float, comment="涨跌幅")
    volume_ratio = Column(Float, comment="量比")
    high_price = Column(Float, comment="最高价")
    low_price = Column(Float, comment="最低价")
    pre_close_price = Column(Float, comment="昨收价")
    volume = Column(Integer, comment="成交量")
    deal_amount = Column(Integer, comment="成交额")
    turnoverrate = Column(Float, comment="换手率")
    listing_date = Column(Date, comment="上市时间")
    industry = Column(String(50), comment="行业")
    area = Column(String(50), comment="地区")
    concept = Column(String(800), comment="概念")
    style = Column(String(255), comment="板块")
    is_hs300 = Column(String(2), comment="沪300")
    is_sz50 = Column(String(2), comment="上证50")
    is_zz500 = Column(String(2), comment="中证500")
    is_zz1000 = Column(String(2), comment="中证1000")
    is_cy50 = Column(String(2), comment="创业板50")
    pe = Column(Float, comment="市盈率")
    pe9 = Column(Float, comment="市盈率TTM")
    pb = Column(Float, comment="市净率")
    ps = Column(Float, comment="市销率")
    itr = Column(Float, comment="存货周转率")
    growth = Column(Float, comment="营收增长率")
    roi = Column(Float, comment="投资回报率")
    roe = Column(Float, comment="净资产收益率")
    total_market_cap = Column(Integer, comment="总市值")
    free_cap = Column(Integer, comment="流通市值")
    total_shares = Column(Integer, comment="总股本")
    free_shares = Column(Integer, comment="流通股本")
    created_at = Column(DateTime, comment="创建时间")
    win_market_5days = Column(BIT, comment="近期跑赢大盘近5日")
    win_market_10days = Column(BIT, comment="近期跑赢大盘近10日")
    win_market_20days = Column(BIT, comment="近期跑赢大盘近20日")
    win_market_30days = Column(BIT, comment="近期跑赢大盘近30日")
    net_inflow = Column(Float, comment="当日净流入额")
    netinflow_3days = Column(Integer, comment="3日主力净流入")
    netinflow_5days = Column(Integer, comment="5日主力净流入")
    nowinterst_ratio = Column(Integer, comment="当日增仓占比")
    nowinterst_ratio_3d = Column(Float, comment="3日增仓占比")
    nowinterst_ratio_5d = Column(Float, comment="5日增仓占比")
    ddx = Column(Float, comment="当日DDX")
    ddx_3d = Column(Float, comment="3日DDX")
    ddx_5d = Column(Float, comment="5日DDX")
    ddx_red_10d = Column(SmallInteger, comment="10日内DDX飘红天数")
    changerate_3days = Column(Float, comment="3日涨跌幅")
    changerate_5days = Column(Float, comment="5日涨跌幅")
    changerate_10days = Column(Float, comment="10日涨跌幅")
    changerate_ty = Column(Float, comment="今年以来涨跌幅")
    upnday = Column(SmallInteger, comment="连涨天数")
    downnday = Column(SmallInteger, comment="连跌天数")
    listing_yield_year = Column(Float, comment="上市以来年化收益率")
    listing_volatility_year = Column(Float, comment="上市以来年化波动率")
    mutual_netbuy_amt = Column(Integer, comment="沪深股通净买入金额")
    hold_ratio = Column(Float, comment="沪深股通持股比例")
    secucode = Column(String(10), comment="全代码")
    fund_amount_super = Column(Integer, comment="超大单净额")
    fund_rate_super = Column(Float, comment="超大单净占比")
    fund_amount_large = Column(Integer, comment="大单净额")
    fund_rate_large = Column(Float, comment="大单净占比")
    fund_amount_medium = Column(Integer, comment="中单净额")
    fund_rate_medium = Column(Float, comment="中单净占比")
    fund_amount_small = Column(Integer, comment="小单净额")
    fund_rate_small = Column(Float, comment="小单净占比")
    fund_amount_3days = Column(Integer, comment="3日主力净额")
    fund_rate_3days = Column(Float, comment="3日主力净占比")
    fund_amount_5days = Column(Integer, comment="5日主力净额")
    fund_rate_5days = Column(Float, comment="5日主力净占比")
    fund_amount_10days = Column(Integer, comment="10日主力净额")
    fund_rate_10days = Column(Float, comment="10日主力净占比")
    is_st = Column(String(2), comment="是否ST")
    pettmdeducted = Column(Float, comment="扣非市盈率TTM")
    ps9 = Column(Float, comment="市销率TTM")
    pcfjyxjl9 = Column(Float, comment="市现率TTM")
    predict_pe_syear = Column(Float, comment="预测市盈率(本年)")
    predict_pe_nyear = Column(Float, comment="预测市盈率(次年)")
    enterprise_value_multiple = Column(Float, comment="企业价值倍数")
    ycpeg = Column(Float, comment="预测PEG")
    per_netcash_operate = Column(Float, comment="每股经营现金流")
    per_fcfe = Column(Float, comment="每股自由现金流")
    per_surplus_reserve = Column(Float, comment="每股盈余公积")
    per_retained_earning = Column(Float, comment="每股未分配利润")
    deduct_netprofit = Column(Float, comment="扣非净利润")
    jroa = Column(Float, comment="加权平均总资产收益率")
    roic = Column(Float, comment="投入资本回报率")
    zxgxl = Column(Float, comment="资金贡献率")
    sale_npr = Column(Float, comment="销售净利率")
    deduct_netprofit_growthrate = Column(Float, comment="扣非净利润增长率")
    netprofit_growthrate_3y = Column(Float, comment="净利润3年复合增长率")
    income_growthrate_3y = Column(Float, comment="营收3年复合增长率")
    predict_netprofit_ratio = Column(Float, comment="预测净利润增长率")
    predict_income_ratio = Column(Float, comment="预测营收增长率")
    basiceps_yoy_ratio = Column(Float, comment="每股收益同比增长率")
    total_profit_growthrate = Column(Float, comment="利润总额同比增长率")
    operate_profit_growthrate = Column(Float, comment="营业利润同比增长率")
    equity_ratio = Column(Float, comment="权益比率")
    equity_multiplier = Column(Float, comment="权益乘数")
    current_ratio = Column(Float, comment="流动比率")
    speed_ratio = Column(Float, comment="速动比率")
    holder_newest = Column(Integer, comment="最新股东户数")
    hold_amount = Column(Float, comment="机构持股金额")
    avg_hold_num = Column(Float, comment="户均持股数")
    holdnum_growthrate_3q = Column(Float, comment="股东户数季度环比")
    holdnum_growthrate_hy = Column(Float, comment="股东户数半年环比")
    hold_ratio_count = Column(Integer, comment="机构持股家数")
    free_hold_ratio = Column(Float, comment="流通股东占比")
    macd_golden_fork = Column(SmallInteger, comment="MACD金叉")
    macd_golden_forkz = Column(SmallInteger, comment="MACD零轴金叉")
    macd_golden_forky = Column(SmallInteger, comment="MACD远离零轴金叉")
    kdj_golden_fork = Column(SmallInteger, comment="KDJ金叉")
    kdj_golden_forkz = Column(SmallInteger, comment="KDJ零轴金叉")
    kdj_golden_forky = Column(SmallInteger, comment="KDJ远离零轴金叉")
    break_through = Column(SmallInteger, comment="突破")
    low_funds_inflow = Column(SmallInteger, comment="低位资金流入")
    high_funds_outflow = Column(SmallInteger, comment="高位资金流出")
    breakup_ma_5days = Column(SmallInteger, comment="突破5日均线")
    breakup_ma_10days = Column(SmallInteger, comment="突破10日均线")
    breakup_ma_20days = Column(SmallInteger, comment="突破20日均线")
    breakup_ma_30days = Column(SmallInteger, comment="突破30日均线")
    breakup_ma_60days = Column(SmallInteger, comment="突破60日均线")
    long_avg_array = Column(SmallInteger, comment="长均线多头排列")
    short_avg_array = Column(SmallInteger, comment="短均线多头排列")
    upper_large_volume = Column(SmallInteger, comment="放量上涨")
    down_narrow_volume = Column(SmallInteger, comment="缩量下跌")
    one_dayang_line = Column(SmallInteger, comment="一阳穿三线")
    two_dayang_lines = Column(SmallInteger, comment="两阳穿三线")
    rise_sun = Column(SmallInteger, comment="旭日东升")
    power_fulgun = Column(SmallInteger, comment="火力全开")
    restore_justice = Column(SmallInteger, comment="绝地反击")
    down_7days = Column(SmallInteger, comment="连续7日下跌")
    upper_8days = Column(SmallInteger, comment="连续8日上涨")
    upper_9days = Column(SmallInteger, comment="连续9日上涨")
    upper_4days = Column(SmallInteger, comment="连续4日上涨")
    heaven_rule = Column(SmallInteger, comment="天量天价")
    upside_volume = Column(SmallInteger, comment="放量")
    bearish_engulfing = Column(SmallInteger, comment="看跌吞没")
    reversing_hammer = Column(SmallInteger, comment="锤子线")
    shooting_star = Column(SmallInteger, comment="流星线")
    evening_star = Column(SmallInteger, comment="黄昏之星")
    first_dawn = Column(SmallInteger, comment="曙光初现")
    pregnant = Column(SmallInteger, comment="十字胎")
    black_cloud_tops = Column(SmallInteger, comment="乌云盖顶")
    morning_star = Column(SmallInteger, comment="晨星")
    narrow_finish = Column(SmallInteger, comment="收窄")
    limited_lift_f6m = Column(SmallInteger, comment="未来6个月限售股解禁")
    limited_lift_f1y = Column(SmallInteger, comment="未来1年限售股解禁")
    limited_lift_6m = Column(SmallInteger, comment="过去6个月限售股解禁")
    limited_lift_1y = Column(SmallInteger, comment="过去1年限售股解禁")
    directional_seo_1m = Column(SmallInteger, comment="1个月定向增发")
    directional_seo_3m = Column(SmallInteger, comment="3个月定向增发")
    directional_seo_6m = Column(SmallInteger, comment="6个月定向增发")
    directional_seo_1y = Column(SmallInteger, comment="1年定向增发")
    recapitalize_1m = Column(SmallInteger, comment="1个月配股")
    recapitalize_3m = Column(SmallInteger, comment="3个月配股")
    recapitalize_6m = Column(SmallInteger, comment="6个月配股")
    recapitalize_1y = Column(SmallInteger, comment="1年配股")
    equity_pledge_1m = Column(SmallInteger, comment="1个月股权质押")
    equity_pledge_3m = Column(SmallInteger, comment="3个月股权质押")
    equity_pledge_6m = Column(SmallInteger, comment="6个月股权质押")
    equity_pledge_1y = Column(SmallInteger, comment="1年股权质押")
    pledge_ratio = Column(Float, comment="质押比例")
    goodwill_scale = Column(Float, comment="商誉规模")
    goodwill_assets_ratro = Column(Float, comment="商誉占总资产比")
    predict_type = Column(String(20), comment="预测类型")
    par_dividend_pretax = Column(Float, comment="每股税前股息")
    par_dividend = Column(Float, comment="每股股息")
    par_it_equity = Column(Float, comment="每股净资产")
    holder_change_3m = Column(Integer, comment="3个月股东人数变化")
    executive_change_3m = Column(Integer, comment="3个月高管变动")
    org_survey_3m = Column(Integer, comment="3个月机构调研")
    org_rating = Column(String(20), comment="机构评级")
    allcorp_num = Column(Integer, comment="机构持股家数")
    allcorp_fund_num = Column(Integer, comment="基金持股家数")
    allcorp_qs_num = Column(Integer, comment="券商持股家数")
    allcorp_qfii_num = Column(Integer, comment="QFII持股家数")
    allcorp_bx_num = Column(Integer, comment="保险持股家数")
    allcorp_sb_num = Column(Integer, comment="社保持股家数")
    allcorp_xt_num = Column(Integer, comment="信托持股家数")
    allcorp_ratio = Column(Float, comment="机构持股比例")
    allcorp_fund_ratio = Column(Float, comment="基金持股比例")
    allcorp_qs_ratio = Column(Float, comment="券商持股比例")
    allcorp_qfii_ratio = Column(Float, comment="QFII持股比例")
    allcorp_bx_ratio = Column(Float, comment="保险持股比例")
    allcorp_sb_ratio = Column(Float, comment="社保持股比例")
    allcorp_xt_ratio = Column(Float, comment="信托持股比例")
    popularity_rank = Column(Integer, comment="人气排名")
    rank_change = Column(Integer, comment="排名变动")
    upp_days = Column(Integer, comment="连涨天数")
    down_days = Column(Integer, comment="连跌天数")
    new_high = Column(SmallInteger, comment="创新高")
    new_down = Column(SmallInteger, comment="创新低")
    newfans_ratio = Column(Float, comment="新增粉丝占比")
    bigfans_ratio = Column(Float, comment="大V粉丝占比")
    concern_rank_7days = Column(Integer, comment="7日关注排名")
    browse_rank = Column(Integer, comment="浏览排名")
    amplitude = Column(Float, comment="振幅")
    is_issue_break = Column(SmallInteger, comment="发行价破发")
    is_bps_break = Column(SmallInteger, comment="净资产破发")
    now_newhigh = Column(SmallInteger, comment="盘中新高")
    now_newlow = Column(SmallInteger, comment="盘中新低")
    high_recent_3days = Column(SmallInteger, comment="3日新高")
    high_recent_5days = Column(SmallInteger, comment="5日新高")
    high_recent_10days = Column(SmallInteger, comment="10日新高")
    high_recent_20days = Column(SmallInteger, comment="20日新高")
    high_recent_30days = Column(SmallInteger, comment="30日新高")
    low_recent_3days = Column(SmallInteger, comment="3日新低")
    low_recent_5days = Column(SmallInteger, comment="5日新低")
    low_recent_10days = Column(SmallInteger, comment="10日新低")
    low_recent_20days = Column(SmallInteger, comment="20日新低")
    low_recent_30days = Column(SmallInteger, comment="30日新低")
    win_market_3days = Column(SmallInteger, comment="3日跑赢大盘")


class StockIndicator(Base):
    """股票指标数据"""

    __tablename__ = "cn_stock_indicators"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    close = Column(Float, comment="价格")
    macd = Column(Float, comment="dif")
    macds = Column(Float, comment="macd")
    macdh = Column(Float, comment="histogram")
    kdjk = Column(Float, comment="kdjk")
    kdjd = Column(Float, comment="kdjd")
    kdjj = Column(Float, comment="kdjj")
    boll_ub = Column(Float, comment="boll上轨")
    boll = Column(Float, comment="boll")
    boll_lb = Column(Float, comment="boll下轨")
    trix = Column(Float, comment="trix")
    trix_20_sma = Column(Float, comment="trma")
    tema = Column(Float, comment="tema")
    cr = Column(Float, comment="cr")
    cr_ma1 = Column(Float, comment="cr_ma1")
    cr_ma2 = Column(Float, comment="cr_ma2")
    cr_ma3 = Column(Float, comment="cr_ma3")
    rsi_6 = Column(Float, comment="rsi_6")
    rsi_12 = Column(Float, comment="rsi_12")
    rsi = Column(Float, comment="rsi")
    rsi_24 = Column(Float, comment="rsi_24")
    vr = Column(Float, comment="vr")
    vr_6_sma = Column(Float, comment="mavr")
    roc = Column(Float, comment="roc")
    rocma = Column(Float, comment="rocma")
    rocema = Column(Float, comment="rocema")
    pdi = Column(Float, comment="pdi")
    mdi = Column(Float, comment="mdi")
    dx = Column(Float, comment="dx")
    adx = Column(Float, comment="adx")
    adxr = Column(Float, comment="adxr")
    wr_6 = Column(Float, comment="wr_6")
    wr_10 = Column(Float, comment="wr_10")
    wr_14 = Column(Float, comment="wr_14")
    cci = Column(Float, comment="cci")
    cci_84 = Column(Float, comment="cci_84")
    tr = Column(Float, comment="tr")
    atr = Column(Float, comment="atr")
    dma = Column(Float, comment="dma")
    dma_10_sma = Column(Float, comment="ama")
    obv = Column(Float, comment="obv")
    sar = Column(Float, comment="sar")
    psy = Column(Float, comment="psy")
    psyma = Column(Float, comment="psyma")
    br = Column(Float, comment="br")
    ar = Column(Float, comment="ar")
    emv = Column(Float, comment="emv")
    emva = Column(Float, comment="emva")
    bias = Column(Float, comment="bias")
    mfi = Column(Float, comment="mfi")
    mfisma = Column(Float, comment="mfisma")
    vwma = Column(Float, comment="vwma")
    mvwma = Column(Float, comment="mvwma")
    ppo = Column(Float, comment="ppo")
    ppos = Column(Float, comment="ppos")
    ppoh = Column(Float, comment="ppoh")
    wt1 = Column(Float, comment="wt1")
    wt2 = Column(Float, comment="wt2")
    supertrend_ub = Column(Float, comment="supertrend_ub")
    supertrend = Column(Float, comment="supertrend")
    supertrend_lb = Column(Float, comment="supertrend_lb")
    dpo = Column(Float, comment="dpo")
    madpo = Column(Float, comment="madpo")
    vhf = Column(Float, comment="vhf")
    rvi = Column(Float, comment="rvi")
    rvis = Column(Float, comment="rvis")
    fi = Column(Float, comment="fi")
    force_2 = Column(Float, comment="force_2")
    force_13 = Column(Float, comment="force_13")
    ene_ue = Column(Float, comment="ene上轨")
    ene = Column(Float, comment="ene")
    ene_le = Column(Float, comment="ene下轨")
    stochrsi_k = Column(Float, comment="stochrsi_k")
    stochrsi_d = Column(Float, comment="stochrsi_d")
    ma5 = Column(Float, comment="MA5")
    ma10 = Column(Float, comment="MA10")
    ma20 = Column(Float, comment="MA20")
    ma30 = Column(Float, comment="MA30")
    ma60 = Column(Float, comment="MA60")
    ma120 = Column(Float, comment="MA120")
    ma250 = Column(Float, comment="MA250")
    volume_ratio_1m = Column(Float, comment="量比1分钟")
    volume_ratio_3m = Column(Float, comment="量比3分钟")
    volume_ratio_5m = Column(Float, comment="量比5分钟")
    volume_ratio_10m = Column(Float, comment="量比10分钟")
    volume_ratio_15m = Column(Float, comment="量比15分钟")
    volume_ratio_30m = Column(Float, comment="量比30分钟")
    volume_ratio_1h = Column(Float, comment="量比1小时")
    volume_ratio_2h = Column(Float, comment="量比2小时")
    volume_ratio_4h = Column(Float, comment="量比4小时")
    volume_ratio_1d = Column(Float, comment="量比1天")
    created_at = Column(DateTime, comment="创建时间")


class StockKlinePattern(Base):
    """股票K线形态"""

    __tablename__ = "cn_stock_pattern"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    tow_crows = Column(SmallInteger, comment="两只乌鸦")
    upside_gap_two_crows = Column(SmallInteger, comment="向上跳空的两只乌鸦")
    three_black_crows = Column(SmallInteger, comment="三只乌鸦")
    identical_three_crows = Column(SmallInteger, comment="胞胎乌鸦")
    three_line_strike = Column(SmallInteger, comment="三线打击")
    morning_star = Column(SmallInteger, comment="早晨之星")
    evening_star = Column(SmallInteger, comment="黄昏之星")
    evening_doji_star = Column(SmallInteger, comment="十字黄昏星")
    doji_star = Column(SmallInteger, comment="十字星")
    three_white_soldiers = Column(SmallInteger, comment="三白兵")
    dark_cloud_cover = Column(SmallInteger, comment="乌云盖顶")
    engulfing = Column(SmallInteger, comment="吞噬")
    harami = Column(SmallInteger, comment="孕线")
    harami_cross = Column(SmallInteger, comment="十字孕线")
    dragonfly_doji = Column(SmallInteger, comment="蜻蜓十字")
    gravestone_doji = Column(SmallInteger, comment="墓碑十字")
    hammer = Column(SmallInteger, comment="锤子线")
    hanging_man = Column(SmallInteger, comment="上吊线")
    inverted_hammer = Column(SmallInteger, comment="倒锤子线")
    shooting_star = Column(SmallInteger, comment="流星线")
    marubozu = Column(SmallInteger, comment="光头光脚/缺影线")
    piercing = Column(SmallInteger, comment="刺透形态")
    counterattack = Column(SmallInteger, comment="反击线形态")
    separating_lines = Column(SmallInteger, comment="分离线形态")
    kicking = Column(SmallInteger, comment="反冲形态")
    stick_sandwich = Column(SmallInteger, comment="条形三明治")
    unique_three_river = Column(SmallInteger, comment="奇特三河床")
    concealing_baby_swallow = Column(SmallInteger, comment="藏婴吞没")
    tri_star = Column(SmallInteger, comment="三星")
    breakaway = Column(SmallInteger, comment="脱离")
    on_neck = Column(SmallInteger, comment="颈上线")
    in_neck = Column(SmallInteger, comment="颈内线")
    thrusting = Column(SmallInteger, comment="插入")
    spinning_top = Column(SmallInteger, comment="纺锤")
    long_line = Column(SmallInteger, comment="长蜡烛")
    short_line = Column(SmallInteger, comment="短蜡烛")
    gap_side_side_white = Column(SmallInteger, comment="并列阳线")
    gap_side_side_black = Column(SmallInteger, comment="并列阴线")
    homing_pigeon = Column(SmallInteger, comment="家鸽")
    matching_low = Column(SmallInteger, comment="相同低价")
    mat_hold = Column(SmallInteger, comment="铺垫")
    rising_falling_three = Column(SmallInteger, comment="上升/下降三法")
    morning_doji_star = Column(SmallInteger, comment="十字晨星")
    abandoned_baby = Column(SmallInteger, comment="弃婴")
    belt_hold = Column(SmallInteger, comment="捉腰带线")
    rickshaw_man = Column(SmallInteger, comment="黄包车夫")
    modified_three_river = Column(SmallInteger, comment="修正三河床")
    advance_block = Column(SmallInteger, comment="大敌当前")
    ladder_bottom = Column(SmallInteger, comment="梯底")
    closing_marubozu = Column(SmallInteger, comment="收盘缺影线")
    tasuki_gap = Column(SmallInteger, comment="跳空并列线")
    side_by_side_white = Column(SmallInteger, comment="并列阴阳线")
    hikkake_pattern = Column(SmallInteger, comment="陷阱形态")
    modified_hikkake_pattern = Column(SmallInteger, comment="修正陷阱形态")
    in_neck_pattern = Column(SmallInteger, comment="颈内线形态")
    on_neck_pattern = Column(SmallInteger, comment="颈上线形态")
    thrusting_pattern = Column(SmallInteger, comment="插入形态")
    piercing_pattern = Column(SmallInteger, comment="刺透形态")
    meeting_lines = Column(SmallInteger, comment="会议线形态")
    stalled_pattern = Column(SmallInteger, comment="停顿形态")
    three_inside_up = Column(SmallInteger, comment="三内部上涨")
    three_inside_down = Column(SmallInteger, comment="三内部下跌")
    three_outside_up = Column(SmallInteger, comment="三外部上涨")
    three_outside_down = Column(SmallInteger, comment="三外部下跌")
    created_at = Column(DateTime, comment="创建时间")
    high_wave_candle = Column(SmallInteger, comment="长影线")
    separating_lines_pattern = Column(SmallInteger, comment="分离线形态")
    three_stars_in_south = Column(SmallInteger, comment="南方三星")
    downside_gap_three_methods = Column(SmallInteger, comment="跳空三法下跌")
    upside_gap_three_methods = Column(SmallInteger, comment="跳空三法上涨")
    engulfing_pattern = Column(SmallInteger, comment="吞噬形态")
    three_stars_in_north = Column(SmallInteger, comment="北方三星")
    identical_three_methods = Column(SmallInteger, comment="三法同线")
    three_methods = Column(SmallInteger, comment="三法形态")
    unique_three_methods = Column(SmallInteger, comment="独特三法")
    three_line_strike_pattern = Column(SmallInteger, comment="三线打击形态")
    three_black_crows_pattern = Column(SmallInteger, comment="三只乌鸦形态")
    three_white_soldiers_pattern = Column(SmallInteger, comment="三白兵形态")
    doji = Column(SmallInteger, comment="十字线")
    up_down_gap = Column(SmallInteger, comment="跳空缺口")
    long_legged_doji = Column(SmallInteger, comment="长脚十字")
    three_inside_up_down = Column(SmallInteger, comment="三内部上下")
    three_outside_up_down = Column(SmallInteger, comment="三外部上下")
    three_stars_in_the_south = Column(SmallInteger, comment="南方三星形态")
    harami_pattern = Column(SmallInteger, comment="孕线形态")
    harami_cross_pattern = Column(SmallInteger, comment="十字孕线形态")
    kicking_bull_bear = Column(SmallInteger, comment="牛熊反冲形态")
    long_line_candle = Column(SmallInteger, comment="长蜡烛线")
    short_line_candle = Column(SmallInteger, comment="短蜡烛线")
    takuri = Column(SmallInteger, comment="探水竿")
    tristar_pattern = Column(SmallInteger, comment="三星形态")
    unique_3_river = Column(SmallInteger, comment="奇特三河")
    upside_downside_gap = Column(SmallInteger, comment="跳空缺口形态")


class StockTop(Base):
    """龙虎榜数据"""

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
    created_at = Column(DateTime, comment="创建时间")


class StockFundFlowIndustry(Base):
    """行业资金流向"""

    __tablename__ = "cn_stock_fund_flow_industry"

    date = Column(Date, primary_key=True, comment="日期")
    industry = Column(String(20), primary_key=True, comment="行业名称")
    change_rate = Column(Float, comment="涨跌幅")
    fund_amount = Column(Integer, comment="主力净流入-净额")
    fund_rate = Column(Float, comment="主力净流入-净占比")
    fund_amount_super = Column(Integer, comment="超大单净流入-净额")
    fund_rate_super = Column(Float, comment="超大单净流入-净占比")
    fund_amount_large = Column(Integer, comment="大单净流入-净额")
    fund_rate_large = Column(Float, comment="大单净流入-净占比")
    fund_amount_medium = Column(Integer, comment="中单净流入-净额")
    fund_rate_medium = Column(Float, comment="中单净流入-净占比")
    fund_amount_small = Column(Integer, comment="小单净流入-净额")
    fund_rate_small = Column(Float, comment="小单净流入-净占比")
    stock_count = Column(Integer, comment="股票数量")
    created_at = Column(DateTime, comment="创建时间")


class StockFundFlowConcept(Base):
    """概念资金流向"""

    __tablename__ = "cn_stock_fund_flow_concept"

    date = Column(Date, primary_key=True, comment="日期")
    concept = Column(String(50), primary_key=True, comment="概念名称")
    change_rate = Column(Float, comment="涨跌幅")
    fund_amount = Column(Integer, comment="主力净流入-净额")
    fund_rate = Column(Float, comment="主力净流入-净占比")
    fund_amount_super = Column(Integer, comment="超大单净流入-净额")
    fund_rate_super = Column(Float, comment="超大单净流入-净占比")
    fund_amount_large = Column(Integer, comment="大单净流入-净额")
    fund_rate_large = Column(Float, comment="大单净流入-净占比")
    fund_amount_medium = Column(Integer, comment="中单净流入-净额")
    fund_rate_medium = Column(Float, comment="中单净流入-净占比")
    fund_amount_small = Column(Integer, comment="小单净流入-净额")
    fund_rate_small = Column(Float, comment="小单净流入-净占比")
    stock_count = Column(Integer, comment="股票数量")
    created_at = Column(DateTime, comment="创建时间")


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


class StockIndicatorsSell(Base):
    """股票卖出指标"""

    __tablename__ = "cn_stock_indicators_sell"

    date = Column(Date, primary_key=True, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    name = Column(String(20), comment="名称")
    close = Column(Float, comment="收盘价")
    ma5 = Column(Float, comment="5日均线")
    ma10 = Column(Float, comment="10日均线")
    ma20 = Column(Float, comment="20日均线")
    ma30 = Column(Float, comment="30日均线")
    ma60 = Column(Float, comment="60日均线")
    ma120 = Column(Float, comment="120日均线")
    ma250 = Column(Float, comment="250日均线")
    vol5 = Column(Float, comment="5日成交量均线")
    vol10 = Column(Float, comment="10日成交量均线")
    vol20 = Column(Float, comment="20日成交量均线")
    vol30 = Column(Float, comment="30日成交量均线")
    vol60 = Column(Float, comment="60日成交量均线")
    vol120 = Column(Float, comment="120日成交量均线")
    vol250 = Column(Float, comment="250日成交量均线")
    rsi6 = Column(Float, comment="6日RSI")
    rsi12 = Column(Float, comment="12日RSI")
    rsi24 = Column(Float, comment="24日RSI")
    macd = Column(Float, comment="MACD")
    macds = Column(Float, comment="MACD信号线")
    macdh = Column(Float, comment="MACD柱状图")
    kdjk = Column(Float, comment="KDJ-K值")
    kdjd = Column(Float, comment="KDJ-D值")
    kdjj = Column(Float, comment="KDJ-J值")
    boll = Column(Float, comment="布林中轨")
    boll_ub = Column(Float, comment="布林上轨")
    boll_lb = Column(Float, comment="布林下轨")
    volume_ratio = Column(Float, comment="量比")
    turnover = Column(Float, comment="换手率")
    created_at = Column(DateTime, comment="创建时间")


if __name__ == "__main__":
    init_db()
