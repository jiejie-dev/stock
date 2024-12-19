from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import logging

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
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False,
)

# 创建会话工厂
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 创建线程安全的会话工厂
session_factory = scoped_session(SessionLocal)

# 导入所有模型
from .models.base import Base
from .models.attention import StockAttention
from .models.etf import StockETFSpot
from .models.spot import StockSpot, StockSpotBuy
from .models.fund_flow import StockFundFlow, StockFundFlowConcept, StockFundFlowIndustry
from .models.block_trade import StockBlockTrade
from .models.indicators import StockIndicatorsSell
from .models.bonus import StockBonus
from .models.top import StockTop

# 导出数据库工具函数
from .utils import init_db, get_db, get_engine, DatabaseSession

__all__ = [
    "Base",
    "StockAttention",
    "StockETFSpot",
    "StockSpot",
    "StockSpotBuy",
    "StockFundFlow",
    "StockFundFlowConcept",
    "StockFundFlowIndustry",
    "StockBlockTrade",
    "StockIndicatorsSell",
    "StockBonus",
    "StockTop",
    "init_db",
    "get_db",
    "get_engine",
    "DatabaseSession",
]
