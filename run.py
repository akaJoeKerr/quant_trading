from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp
from vnpy_ctabacktester import CtaBacktesterApp
from vnpy_datamanager import DataManagerApp
from vnpy_riskmanager import RiskManagerApp
from vnpy_webtrader import WebTraderApp
from vnpy_chartwizard import ChartWizardApp


def main():
    """启动量化交易平台"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    # 添加交易接口 - CTP 支持 A 股和 ETF 期权
    main_engine.add_gateway(CtpGateway)
    
    # 添加功能模块
    main_engine.add_app(CtaStrategyApp)           # CTA 策略引擎
    main_engine.add_app(CtaBacktesterApp)         # CTA 策略回测
    main_engine.add_app(DataManagerApp)           # 数据管理
    main_engine.add_app(RiskManagerApp)           # 风险管理
    main_engine.add_app(WebTraderApp)             # Web 服务
    main_engine.add_app(ChartWizardApp)           # K 线图表

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
