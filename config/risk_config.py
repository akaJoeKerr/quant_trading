# 风险管理模块配置

## 风险参数

```python
# 最大持仓数量
max_position = 100

# 最大日亏损（元）
max_daily_loss = 10000

# 最大回撤（比例）
max_drawdown = 0.1  # 10%

# 单笔交易最大风险
max_risk_per_trade = 0.02  # 2%

# 总风险暴露
max_total_exposure = 2.0  # 2 倍杠杆

# 止损参数
stop_loss_type = "ATR"  # ATR 或固定价格
stop_loss_multiplier = 2.0  # ATR 倍数

# 止盈参数
take_profit_type = "ATR"
take_profit_multiplier = 3.0

# 仓位管理
position_size_type = "fixed"  # fixed: 固定仓位, risk: 风险仓位
position_size_value = 100000  # 固定仓位价值
risk_ratio = 0.01  # 风险仓位比例

# 资金管理
cash_reserve_ratio = 0.2  # 现金储备比例
max_leverage = 2.0  # 最大杠杆
```

## 风控规则

### 1. 持仓限制

- 单品种最大持仓：100 手
- 总持仓限制：200 手
- 连续亏损限制：5 次

### 2. 价格限制

- 最大涨跌幅限制：20%
- 最大波动率：3σ
- 异常价格过滤：±5%

### 3. 时间限制

- 下单时间窗口：9:00-15:00
- 撤单时间窗口：9:00-15:00
- 收盘前平仓：14:55

### 4. 事件驱动风控

```python
# 事件注册
EVENT_RISK_CHECK = "e.RiskCheck"
EVENT_RISK_LIMIT = "e.RiskLimit"
EVENT_RISK_WARNING = "e.RiskWarning"
```

## 风控日志

```python
# 风控日志级别
LOG_LEVEL = "INFO"

# 风控日志文件
LOG_FILE = "risk.log"
```
