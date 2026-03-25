# Quant Trading - A 股 & ETF 期权量化交易系统

<div align="center">
  <p><b>基于 VeighNa 框架的 A 股与 ETF 期权量化交易平台</b></p>
  <p><i>By Traders, For Traders</i></p>
</div>

## 📋 项目简介

本项目是基于 VeighNa 量化交易框架开发的专用交易系统，专注于**A 股市场**和**ETF 期权**交易，提供完整的量化交易解决方案。

### 核心功能

- ✅ **A 股交易** - 支持沪深 A 股全市场
- ✅ **ETF 期权** - 支持场内 ETF 期权交易
- ✅ **CTA 策略** - 趋势跟踪、均值回归策略
- ✅ **组合策略** - 多标的组合管理
- ✅ **回测系统** - 完整的策略回测功能
- ✅ **实盘交易** - 支持 CTP、XTP、TORA 等接口
- ✅ **风险管理** - 实时风控监控
- ✅ **数据分析** - 集成 Alpha 158 因子库

## 🏗️ 项目架构

```
quant_trading/
├── vnpy/                    # VeighNa 框架
│   ├── trader/              # 交易核心引擎
│   ├── event/               # 事件驱动引擎
│   ├── gateway/             # 交易接口
│   ├── app/                 # 功能模块
│   ├── object/              # 数据对象
│   └── database/            # 数据库适配器
├── strategies/              # 策略目录
│   ├── cta/                 # CTA 策略
│   ├── portfolio/           # 组合策略
│   └── option/              # 期权策略
├── data/                    # 数据管理
│   ├── backtest/            # 回测数据
│   └── real/                # 实盘数据
├── config/                  # 配置文件
├── logs/                    # 日志目录
└── tests/                   # 测试文件
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置交易接口

编辑 `config/gateway.py` 配置你的交易接口：

```python
# CTP 接口配置
gateways["CTP"] = {
    "name": "CTP",
    "password": "your_password",
    "brokerid": "9999",
    "userid": "your_userid",
    "appid": "your_appid",
    "authcode": "your_authcode",
    "product": "CFFEX",
    "variety": "CTP"
}
```

### 3. 启动系统

```bash
# 方式一：使用脚本运行
python run.py

# 方式二：直接运行主引擎
python main.py
```

## 📡 支持的交易接口

### A 股交易接口

| 接口 | 状态 | 说明 |
|------|------|------|
| **中泰 XTP** | ✅ | A 股、ETF 期权首选 |
| **华鑫奇点** | ✅ | A 股、ETF 期权 |
| **东方财富 EMT** | ✅ | A 股交易 |
| **掘金** | ✅ | A 股交易 |

### ETF 期权接口

| 接口 | 状态 | 说明 |
|------|------|------|
| **中泰 XTP** | ✅ | ETF 期权专用 |
| **华鑫奇点** | ✅ | ETF 期权专用 |
| **顶点 HTS** | ✅ | ETF 期权 |
| **顶点飞创** | ✅ | ETF 期权 |

## 🎯 核心策略

### 1. CTA 趋势跟踪策略

```python
from vnpy_ctastrategy import CtaStrategyApp

class TrendFollowingStrategy(CtaStrategyApp):
    """趋势跟踪策略"""
    
    def on_init(self):
        self.params = {
            "boll_period": 20,
            "rsi_period": 14,
            "ma_period": 20
        }
    
    def on_bar(self, bar: BarData):
        # 趋势跟踪逻辑
        pass
```

### 2. 期权策略

```python
class OptionStrategy(CtaStrategyApp):
    """期权策略"""
    
    def on_tick(self, tick: TickData):
        # 期权定价与对冲逻辑
        pass
```

### 3. 组合策略

```python
class PortfolioStrategy(Strategy):
    """多标的组合策略"""
    
    def on_bar(self, bar: BarData):
        # 组合管理逻辑
        pass
```

## 📊 回测系统

```python
from vnpy_ctabacktester import CtaBacktesterApp

# 创建回测引擎
backtester = CtaBacktesterApp()

# 配置回测参数
backtester.set_parameters(
    vt_symbol="510300.CSH",  # ETF 代码
    interval="1m",           # K 线周期
    backtesting_start="20230101",
    backtesting_end="20231231",
    hot_start=True
)

# 运行回测
backtester.run(strategy)
```

## 📈 风险管理

```python
from vnpy_riskmanager import RiskManager

# 创建风险管理系统
risk_manager = RiskManager()

# 设置风控规则
risk_manager.set_parameters(
    max_position=100,        # 最大持仓
    max_loss=10000,          # 最大亏损
    max_drawdown=0.1,        # 最大回撤
    daily_limit=50000        # 日限额
)
```

## 📚 数据管理

```python
from vnpy_datamanager import DataManager

# 创建数据管理器
data_manager = DataManager()

# 导入历史数据
data_manager.import_data(
    vt_symbol="510300.CSH",
    interval="1m",
    start="20230101",
    end="20231231"
)
```

## 🔧 配置文件

### config/gateway.py

```python
from vnpy.trader.setting import SETTINGS

SETTINGS["gateway.1.name"] = "CTP"
SETTINGS["gateway.1.type"] = "CTP"
SETTINGS["gateway.1.password"] = ""
SETTINGS["gateway.1.brokerid"] = "9999"
SETTINGS["gateway.1.userid"] = ""
SETTINGS["gateway.1.appid"] = ""
SETTINGS["gateway.1.authcode"] = ""
SETTINGS["gateway.1.product"] = "CFFEX"
SETTINGS["gateway.1.variety"] = "CTP"
```

### config/setting.py

```python
SETTINGS = {
    "font.family": "SimHei",
    "font.size": 12,
    "log.active": True,
    "log.file": True,
    "log.file_name": "log",
    "log.file_path": "./logs",
    "log.file_size": 10485760,
    "log.max_files": 10,
    "log.datetime_format": "%Y-%m-%d %H:%M:%S",
    "log.level": "INFO",
    "log.time": True,
    "email.server": "",
    "email.port": 25,
    "email.username": "",
    "email.password": "",
    "email.sender": "",
    "email.receiver": "",
    "database": "sqlite",
    "database.path": "./data.db",
    "trader.name": "",
    "trader.dir": "./trader",
    "trader.web": "",
    "trader.ui": "qt",
    "trader.setting": "setting.json",
    "trader.log": "log.json",
    "trader.error": "error.log",
    "trader.app": "app.json",
    "trader.gateway": "gateway.json",
    "trader.database": "database.json",
    "trader.datafeed": "datafeed.json",
    "trader.risk": "risk.json",
    "trader.web": "web.json",
    "trader.ui": "ui.json",
    "trader.rpc": "rpc.json",
    "trader.chart": "chart.json",
    "trader.data": "data.json",
    "trader.risk": "risk.json",
    "trader.web": "web.json",
    "trader.ui": "ui.json",
    "trader.rpc": "rpc.json",
    "trader.chart": "chart.json",
    "trader.data": "data.json",
}
```

## 📝 运行示例

### 主引擎启动

```python
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
    
    # 添加交易接口
    main_engine.add_gateway(CtpGateway)
    
    # 添加功能模块
    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)
    main_engine.add_app(DataManagerApp)
    main_engine.add_app(RiskManagerApp)
    main_engine.add_app(WebTraderApp)
    main_engine.add_app(ChartWizardApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
```

## 🧪 测试文件

### tests/test_strategy.py

```python
import unittest
from unittest.mock import Mock

from vnpy.trader.object import BarData, TickData


class TestStrategy(unittest.TestCase):
    
    def test_on_bar(self):
        """测试 K 线回调"""
        strategy = Mock()
        bar = BarData(
            symbol="510300",
            exchange="SHFE",
            vt_symbol="510300+SHFE",
            name="沪深 300ETF",
            datetime=None,
            interval="1m",
            volume=0,
            open_interest=0,
            open_price=0,
            high_price=0,
            low_price=0,
            close_price=0,
            gateway_name="CTP"
        )
        strategy.on_bar(bar)
        
    def test_on_tick(self):
        """测试 Tick 回调"""
        tick = TickData(
            symbol="510300",
            exchange="SHFE",
            vt_symbol="510300+SHFE",
            name="沪深 300ETF",
            last_price=3.5,
            last_volume=100,
            limit_price=3.4,
            bid_price=3.4,
            bid_volume=10,
            ask_price=3.6,
            ask_volume=10,
            open_interest=100,
            direction="",
            force_close=False,
            timestamp=1234567890000.0,
            datetime=1234567890000.0,
            gateway_name="CTP"
        )
        strategy.on_tick(tick)


if __name__ == "__main__":
    unittest.main()
```

## 📊 回测结果分析

```python
# 回测完成后获取结果
result = backtester.get_result()

# 获取收益曲线
pnl_curve = result.pnl_curve

# 获取交易记录
trades = result.trades

# 获取统计指标
stats = result.stats
print(f"总收益：{stats['total_pnl']}")
print(f"最大回撤：{stats['max_drawdown']}")
print(f"夏普比率：{stats['sharpe_ratio']}")
```

## 📚 数据源

### 历史数据

- **迅投研** - A 股、ETF、期权数据
- **RQData** - 跨市场数据
- **TuShare** - 开源数据
- **Wind** - 专业金融数据

### 实时行情

- **CTP** - 实时行情推送
- **XTP** - 实时行情推送
- **TORA** - 实时行情推送

## 🔐 安全配置

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$pyenv
venv/
.env

# VeighNa
.trader/
*.db
*.sqlite
*.sqlite3
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# 配置文件
config/*.json
config/*.yaml

# 数据文件
data/*.csv
data/*.h5
data/*.parquet

# 日志文件
logs/*.log
```

## 📖 文档资源

- **VeighNa 官方文档**: https://www.vnpy.com/docs/cn/index.html
- **社区论坛**: https://www.vnpy.com/forum/
- **GitHub**: https://github.com/vnpy/vnpy

## 🎯 项目特色

- ✅ **专注 A 股与 ETF 期权** - 专为 A 股市场设计
- ✅ **完整的交易链路** - 从回测到实盘
- ✅ **风险管理** - 内置风控系统
- ✅ **多接口支持** - 支持主流交易接口
- ✅ **数据管理** - 完整的数据管理工具
- ✅ **可视化界面** - 图形化操作界面

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Made with ❤️ by VeighNa Team**
