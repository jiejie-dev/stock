from sqlalchemy import Column, String, DateTime
from .base import Base


class StockAttention(Base):
    """我的关注"""

    __tablename__ = "cn_stock_attention"

    datetime = Column(DateTime, comment="日期")
    code = Column(String(6), primary_key=True, comment="代码")
    created_at = Column(DateTime, comment="创建时间")
