#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
环境变量检查脚本
用于检查数据库连接相关的环境变量配置
"""

import os
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def check_environment_variables():
    """检查环境变量"""
    logging.info("开始检查环境变量...")

    # 数据库相关环境变量
    db_vars = {
        "db_host": "数据库主机地址",
        "db_user": "数据库用户名",
        "db_password": "数据库密码",
        "db_database": "数据库名称",
        "db_port": "数据库端口",
    }

    missing_vars = []
    present_vars = {}

    for var_name, description in db_vars.items():
        value = os.environ.get(var_name)
        if value is not None:
            if var_name == "db_password":
                # 密码只显示长度，不显示内容
                display_value = "*" * len(value)
            else:
                display_value = value
            present_vars[var_name] = value
            logging.info(f"✓ {var_name} ({description}): {display_value}")
        else:
            missing_vars.append(var_name)
            logging.warning(f"✗ {var_name} ({description}): 未设置")

    # 检查其他可能的环境变量
    other_vars = ["PYTHONPATH", "PATH", "LANG", "LC_ALL"]

    logging.info("\n其他环境变量:")
    for var_name in other_vars:
        value = os.environ.get(var_name)
        if value:
            logging.info(f"✓ {var_name}: {value}")
        else:
            logging.info(f"- {var_name}: 未设置")

    # 总结
    logging.info("\n" + "=" * 50)
    logging.info("环境变量检查总结:")

    if missing_vars:
        logging.warning(f"缺失的环境变量: {', '.join(missing_vars)}")
        logging.warning("请设置这些环境变量以确保数据库连接正常!")
    else:
        logging.info("所有必需的数据库环境变量都已设置!")

    # 构建数据库连接字符串
    if all(
        var in present_vars
        for var in ["db_host", "db_user", "db_password", "db_database", "db_port"]
    ):
        try:
            port = int(present_vars["db_port"])
            connection_string = f"mysql+pymysql://{present_vars['db_user']}:****@{present_vars['db_host']}:{port}/{present_vars['db_database']}?charset=utf8mb4"
            logging.info(f"数据库连接字符串: {connection_string}")
        except ValueError:
            logging.error(f"数据库端口 '{present_vars['db_port']}' 不是有效的数字!")

    logging.info("=" * 50)


def check_python_path():
    """检查Python路径"""
    logging.info("\n检查Python路径...")

    import sys

    logging.info(f"Python版本: {sys.version}")
    logging.info(f"Python可执行文件: {sys.executable}")
    logging.info(f"Python路径:")
    for i, path in enumerate(sys.path):
        logging.info(f"  {i+1}. {path}")


def check_installed_packages():
    """检查已安装的包"""
    logging.info("\n检查已安装的包...")

    try:
        import pkg_resources

        installed_packages = [d.project_name for d in pkg_resources.working_set]

        # 检查关键包
        key_packages = ["sqlalchemy", "pymysql", "pandas", "numpy", "requests"]

        for package in key_packages:
            if package in installed_packages:
                logging.info(f"✓ {package}: 已安装")
            else:
                logging.warning(f"✗ {package}: 未安装")

    except ImportError:
        logging.warning("无法检查已安装的包 (pkg_resources 不可用)")


def main():
    """主函数"""
    logging.info("=" * 50)
    logging.info("环境变量和系统配置检查")
    logging.info("=" * 50)

    check_environment_variables()
    check_python_path()
    check_installed_packages()

    logging.info("\n检查完成!")


if __name__ == "__main__":
    main()
