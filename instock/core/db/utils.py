from . import Base, engine, session_factory
import logging


def init_db():
    """初始化数据库"""
    try:
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


class DatabaseSession:
    """数据库会话上下文管理器"""

    def __init__(self):
        self.db = None

    def __enter__(self):
        self.db = session_factory()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
            logging.error(f"数据库操作异常: {str(exc_val)}")
        self.db.close()
