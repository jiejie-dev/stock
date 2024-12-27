import os.path
import sys

# 在项目运行时，临时将项目路径添加到环境变量
cpath_current = os.path.dirname(os.path.dirname(__file__))
cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
sys.path.append(cpath)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instock.core.db import DATABASE_URL
from flask import jsonify, request
from datetime import datetime
from instock.core import db
from instock.core.db import *
import instock.core.stockfetch as stf
import instock.core.kline.visualization as vis

# 创建 Flask 应用
app = Flask(__name__)

# 配置数据库
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化 SQLAlchemy
db = SQLAlchemy(app)


@app.route("/api/stock", methods=["GET"])
def get_stock_data():
    """获取股票数据"""
    table_name = request.args.get("name")
    date = request.args.get("date", default=datetime.now().strftime("%Y-%m-%d"))
    # 只包含主板参数
    only_main_board = request.args.get("only_main_board", default=False)
    # 市值大于参数
    market_cap_gt = request.args.get("market_cap_gt", default=None)
    # 市值小于参数
    market_cap_lt = request.args.get("market_cap_lt", default=None)
    # 涨跌幅大于参数
    change_rate_gt = request.args.get("change_rate_gt", default=None)
    # 涨跌幅小于参数
    change_rate_lt = request.args.get("change_rate_lt", default=None)
    # 换手率大于参数
    turnover_gt = request.args.get("turnover_gt", default=None)
    # 换手率小于参数
    turnover_lt = request.args.get("turnover_lt", default=None)
    # 市盈率大于参数
    pe_gt = request.args.get("pe_gt", default=None)
    # 市盈率小于参数
    pe_lt = request.args.get("pe_lt", default=None)
    # 市净率大于参数
    pb_gt = request.args.get("pb_gt", default=None)
    # 市净率小于参数
    pb_lt = request.args.get("pb_lt", default=None)
    # 行业参数
    industry = request.args.get("industry", default=None)
    # 概念参数
    concept = request.args.get("concept", default=None)

    # 获取对应的模型类
    model_map = {
        "cn_stock_attention": StockAttention,
        "cn_etf_spot": StockETFSpot,
        "cn_stock_spot": StockSpot,
        "cn_stock_spot_buy": StockSpotBuy,
        "cn_stock_fund_flow": StockFundFlow,
        "cn_stock_fund_flow_concept": StockFundFlowConcept,
        "cn_stock_fund_flow_industry": StockFundFlowIndustry,
        "cn_stock_blocktrade": StockBlockTrade,
        "cn_stock_indicators_sell": StockIndicatorsSell,
        "cn_stock_bonus": StockBonus,
        "cn_stock_top": StockTop,
        "cn_stock_selection": StockSelection,
    }

    model = model_map.get(table_name)
    if not model:
        return jsonify({"error": "Invalid table name"}), 400

    # 构建查询
    query = db.session.query(model)
    if date:
        query = query.filter(model.date == datetime.strptime(date, "%Y-%m-%d").date())
    if only_main_board:
        query = query.filter(
            model.code.startswith("600")
            | model.code.startswith("601")
            | model.code.startswith("603")
            | model.code.startswith("605")
            | model.code.startswith("000")
            | model.code.startswith("001")
            | model.code.startswith("002")
        )
    if market_cap_gt:
        query = query.filter(model.total_market_cap > market_cap_gt)
    if market_cap_lt:
        query = query.filter(model.total_market_cap < market_cap_lt)
    if change_rate_gt:
        query = query.filter(model.change_rate > change_rate_gt)
    if change_rate_lt:
        query = query.filter(model.change_rate < change_rate_lt)
    if turnover_gt:
        query = query.filter(model.turnoverrate > turnover_gt)
    if turnover_lt:
        query = query.filter(model.turnoverrate < turnover_lt)
    if pe_gt:
        query = query.filter(model.pe > pe_gt)
    if pe_lt:
        query = query.filter(model.pe < pe_lt)
    if pb_gt:
        query = query.filter(model.pb > pb_gt)
    if pb_lt:
        query = query.filter(model.pb < pb_lt)
    if industry:
        query = query.filter(model.industry == industry)
    if concept:
        query = query.filter(model.concept == concept)

    # 只查询code,name,new_price,change_rate,volume_ratio,high_price,low_price,pre_close_price,volume,deal_amount,turnoverrate
    query = query.with_entities(
        model.code,
        model.name,
        model.new_price,
        model.change_rate,
        model.volume_ratio,
        model.high_price,
        model.low_price,
        model.pre_close_price,
        model.volume,
        model.deal_amount,
        model.turnoverrate,
    )
    # 执行查询
    results = query.all()

    return jsonify(
        [
            {
                "code": item.code,
                "name": item.name,
                "new_price": item.new_price,
                "change_rate": item.change_rate,
                "volume_ratio": item.volume_ratio,
                "high_price": item.high_price,
                "low_price": item.low_price,
                "pre_close_price": item.pre_close_price,
                "volume": item.volume,
                "deal_amount": item.deal_amount,
                "turnoverrate": item.turnoverrate,
            }
            for item in results
        ]
    )


@app.route("/api/indicators", methods=["GET"])
def get_indicators_data():
    """获取指标数据"""
    code = request.args.get("code")
    date = request.args.get("date")
    name = request.args.get("name")
    comp_list = []
    try:
        if code.startswith(("1", "5")):
            stock = stf.fetch_etf_hist((date, code))
        else:
            stock = stf.fetch_stock_hist((date, code))
        if stock is None:
            return

        pk = vis.get_plot_kline(code, stock, date, name)
        if pk is None:
            return

        comp_list.append(pk)
        return jsonify(comp_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
