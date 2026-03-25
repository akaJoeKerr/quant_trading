# Quant Trading - 量化交易系统

<div align="center">
  <p><b>Quantitative Trading System for A-Share & ETF Options</b></p>
  <p><i>基于 VeighNa 框架的量化交易平台 | Quantitative Trading Platform based on VeighNa</i></p>
</div>

---

## 🚀 Quick Start / 快速开始

### 1️⃣ Environment Setup / 环境准备

```bash
# Create virtual environment / 创建虚拟环境
python -m venv venv

# Activate / 激活
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Install dependencies / 安装依赖
pip install -r requirements.txt
```

### 2️⃣ Configuration / 配置

```bash
# Copy environment template / 复制环境变量模板
cp .env.example .env

# Edit .env with your credentials / 编辑.env 填入账号信息
```

### 3️⃣ Run / 运行

```bash
python run.py
```

---

## 📋 Features / 功能特性

| Feature | Description | 说明 |
|---------|-------------|------|
| 📊 CTA Strategies | Trend following, Mean reversion | CTA 策略：趋势跟踪、均值回归 |
| 🎯 Risk Management | Real-time risk control | 实时风控 |
| 📈 Backtesting | Complete backtest system | 完整回测系统 |
| 🔄 Live Trading | CTP, XTP, TORA support | 实盘交易支持 |
| 📑 Data Management | CSV, Parquet, HDF5 | 数据管理 |

---

## 🏗️ Project Structure / 项目结构

```
quant_trading/
├── config/               # 配置
│   ├── config.yaml      # 统一配置
│   └── gateway.py       # 接口配置
├── strategies/          # 策略
│   ├── cta/
│   │   └── trend_following.py
│   └── data_manager.py
├── risk_manager.py      # 风险管理
├── tests/               # 测试
│   └── test_system.py
├── .env.example         # 环境变量模板
├── requirements.txt     # 依赖
└── run.py              # 启动脚本
```

---

## 🎯 Core Strategies / 核心策略

### Trend Following / 趋势跟踪

```python
# Parameters / 参数
boll_period = 20
atr_period = 14
atr_multiplier = 2

# Logic / 逻辑
- Break above upper band → Long / 突破上轨 → 开多
- Break below lower band → Short / 突破下轨 → 开空
- ATR stop-loss / ATR 止损
```

---

## 📊 Backtesting / 回测

```python
from vnpy_ctabacktester import CtaBacktesterApp

backtester = CtaBacktesterApp()
backtester.set_parameters(
    vt_symbol="510300.CSH",
    interval="1m",
    backtesting_start="20230101",
    backtesting_end="20231231",
    initial_capital=1000000
)

backtester.run(strategy)
```

---

## 🔐 Security / 安全

- ✅ Environment variables for sensitive data / 敏感信息使用环境变量
- ✅ `.env` in `.gitignore` / `.env` 已加入 `.gitignore`
- ✅ No hardcoded passwords / 无硬编码密码

---

## 📚 Documentation / 文档

- [README (Full)](README.md) - 完整文档
- [INSTALL.md](INSTALL.md) - 安装指南
- [OPTIMIZATION_SUGGESTIONS.md](OPTIMIZATION_SUGGESTIONS.md) - 优化建议
- [OPTIMIZATION_PROGRESS.md](OPTIMIZATION_PROGRESS.md) - 优化进度

---

## 🔗 Resources / 资源

- **VeighNa Docs**: https://www.vnpy.com/docs/cn/index.html
- **GitHub**: https://github.com/vnpy/vnpy
- **Forum**: https://www.vnpy.com/forum/

---

## 📝 License / 许可证

MIT License

---

## 🤝 Contributing / 贡献

Issues & Pull Requests welcome! / 欢迎提交 Issue 和 PR！

---

**Made with ❤️ by VeighNa Team**
