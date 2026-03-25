"""
风险管理模块

功能：
1. 实时风控监控
2. 持仓限制检查
3. 价格限制检查
4. 事件驱动风控

使用方式：
1. 在 MainEngine 中注册 RiskManagerApp
2. 在策略中调用 risk_manager.check() 进行风控检查
3. 接收 EVENT_RISK_CHECK 事件进行风控反馈
"""

from vnpy.trader.object import TickData, BarData, OrderData, TradeData, ContractData
from vnpy.trader.event import EVENT_RISK_CHECK, EVENT_RISK_LIMIT, EVENT_RISK_WARNING
from vnpy.trader.utility import now_in_trading_hours
import logging


class RiskManager:
    """
    风险管理系统
    
    继承自 vnpy_riskmanager 或自定义实现
    """
    
    def __init__(self):
        """初始化风险管理系统"""
        # 风险参数
        self.max_position = 100              # 最大持仓数量
        self.max_daily_loss = 10000          # 最大日亏损（元）
        self.max_drawdown = 0.1              # 最大回撤（比例）
        self.max_risk_per_trade = 0.02       # 单笔交易最大风险
        self.max_total_exposure = 2.0        # 总风险暴露
        
        # 止损参数
        self.stop_loss_type = "ATR"          # ATR 或固定价格
        self.stop_loss_multiplier = 2.0      # ATR 倍数
        
        # 止盈参数
        self.take_profit_type = "ATR"
        self.take_profit_multiplier = 3.0
        
        # 仓位管理
        self.position_size_type = "fixed"    # fixed: 固定仓位，risk: 风险仓位
        self.position_size_value = 100000    # 固定仓位价值
        self.risk_ratio = 0.01               # 风险仓位比例
        
        # 资金管理
        self.cash_reserve_ratio = 0.2        # 现金储备比例
        self.max_leverage = 2.0              # 最大杠杆
        
        # 持仓记录
        self.position_record = {}            # {vt_symbol: {"pos": int, "entry_price": float, "unrealized_pnl": float}}
        self.daily_loss = 0.0                # 今日亏损
        self.consecutive_loss = 0            # 连续亏损次数
        
        # 事件注册
        self.event_engine = None
        
    def set_event_engine(self, event_engine):
        """设置事件引擎"""
        self.event_engine = event_engine
        
    def set_parameters(self, **kwargs):
        """设置风险参数"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
    def on_tick(self, tick: TickData):
        """Tick 回调 - 实时风控检查"""
        try:
            # 检查价格异常
            self.check_price_limit(tick)
            
            # 检查持仓限制
            self.check_position_limit(tick)
            
            # 检查日亏损
            self.check_daily_loss(tick)
            
            # 发送风控事件
            self.send_risk_event(tick)
            
        except Exception as e:
            logging.error(f"风控检查错误：{e}")
            
    def on_bar(self, bar: BarData):
        """K 线回调 - 周期风控检查"""
        try:
            # 检查持仓限制
            self.check_position_limit(bar)
            
            # 检查日亏损
            self.check_daily_loss(bar)
            
            # 检查回撤
            self.check_drawdown(bar)
            
        except Exception as e:
            logging.error(f"周期风控检查错误：{e}")
            
    def on_order(self, order: OrderData):
        """委托回调 - 下单前风控检查"""
        try:
            # 检查持仓限制
            self.check_position_limit(order)
            
            # 检查资金限制
            self.check_funding_limit(order)
            
        except Exception as e:
            logging.error(f"下单风控检查错误：{e}")
            
    def on_trade(self, trade: TradeData):
        """成交回调 - 更新持仓记录"""
        try:
            # 更新持仓记录
            self.update_position_record(trade)
            
            # 更新日亏损
            self.update_daily_loss(trade)
            
        except Exception as e:
            logging.error(f"成交处理错误：{e}")
            
    def check_price_limit(self, tick: TickData):
        """检查价格限制"""
        # TODO: 实现价格限制检查逻辑
        pass
        
    def check_position_limit(self, tick: TickData):
        """检查持仓限制"""
        try:
            # 获取合约信息
            contract = self.get_contract(tick.vt_symbol)
            if not contract:
                return
                
            # 获取当前持仓
            current_position = self.position_record.get(tick.vt_symbol, {})
            current_pos = current_position.get("pos", 0)
            
            # 检查是否超过最大持仓
            if abs(current_pos) + 1 > self.max_position:
                self.send_risk_event(
                    tick,
                    EVENT_RISK_LIMIT,
                    f"超过最大持仓限制：当前{current_pos}手，最大{self.max_position}手"
                )
                
        except Exception as e:
            logging.error(f"持仓限制检查错误：{e}")
            
    def check_daily_loss(self, tick: TickData):
        """检查日亏损"""
        try:
            # 计算当前亏损
            if self.daily_loss >= self.max_daily_loss:
                self.send_risk_event(
                    tick,
                    EVENT_RISK_LIMIT,
                    f"超过最大日亏损：当前{self.daily_loss:.2f}元，最大{self.max_daily_loss}元"
                )
                
        except Exception as e:
            logging.error(f"日亏损检查错误：{e}")
            
    def check_drawdown(self, bar: BarData):
        """检查回撤"""
        try:
            # TODO: 实现回撤计算逻辑
            pass
            
        except Exception as e:
            logging.error(f"回撤检查错误：{e}")
            
    def check_funding_limit(self, order: OrderData):
        """检查资金限制"""
        try:
            # TODO: 实现资金限制检查逻辑
            pass
            
        except Exception as e:
            logging.error(f"资金限制检查错误：{e}")
            
    def update_position_record(self, trade: TradeData):
        """更新持仓记录"""
        try:
            vt_symbol = trade.vt_symbol
            
            if vt_symbol not in self.position_record:
                self.position_record[vt_symbol] = {
                    "pos": 0,
                    "entry_price": 0.0,
                    "unrealized_pnl": 0.0
                }
                
            record = self.position_record[vt_symbol]
            
            # 更新持仓
            record["pos"] += 1 if trade.direction == "LONG" else -1
            
            # 更新开仓价格
            if record["pos"] == 1:
                record["entry_price"] = trade.price
                
            # 更新 unrealized PnL
            record["unrealized_pnl"] = (trade.price - record["entry_price"]) * record["pos"]
            
        except Exception as e:
            logging.error(f"持仓记录更新错误：{e}")
            
    def update_daily_loss(self, trade: TradeData):
        """更新日亏损"""
        try:
            # TODO: 实现日亏损计算逻辑
            pass
            
        except Exception as e:
            logging.error(f"日亏损更新错误：{e}")
            
    def send_risk_event(self, data, event_type, message):
        """发送风控事件"""
        if self.event_engine:
            try:
                from vnpy.event import Event
                from vnpy.trader.constant import EventType
                
                event = Event(event_type, data)
                event.data.message = message
                self.event_engine.put(event)
                
            except Exception as e:
                logging.error(f"发送风控事件错误：{e}")
                
    def reset_daily(self):
        """重置日数据"""
        self.daily_loss = 0.0
        self.consecutive_loss = 0
        
    def get_risk_status(self):
        """获取风险状态"""
        return {
            "max_position": self.max_position,
            "current_positions": {k: v["pos"] for k, v in self.position_record.items()},
            "daily_loss": self.daily_loss,
            "max_daily_loss": self.max_daily_loss,
            "consecutive_loss": self.consecutive_loss
        }


# 全局风险管理器实例
risk_manager = RiskManager()
