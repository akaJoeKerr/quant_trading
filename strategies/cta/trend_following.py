"""
CTA 趋势跟踪策略示例

适用于 A 股和 ETF 期权的趋势跟踪策略

**修复说明 (2026-03-25):**
- 替换不存在的 `ArrayTool` 为 VeighNa 标准方式
- 修复 `get_bars()` 方法
- 添加错误处理和日志记录
"""

from vnpy.trader.object import TickData, BarData
from vnpy.trader.strategy import StrategyTemplate
from vnpy.trader.utility import BarGenerator
from vnpy.ctastrategy import CtaStrategyTemplate
import numpy as np


class TrendFollowingStrategy(CtaStrategyTemplate):
    """
    CTA 趋势跟踪策略
    
    策略逻辑：
    1. 使用 Bollinger Bands 判断趋势
    2. 突破上轨开多，突破下轨开空
    3. 使用 ATR 设置止损止盈
    
    适用品种：
    - A 股：沪深 300ETF、中证 500ETF 等
    - ETF 期权：50ETF 期权、300ETF 期权等
    """
    
    def __init__(self, cta_engine, strategy_name, strategy_vt_id=None):
        """初始化策略"""
        super().__init__(cta_engine, strategy_name, strategy_vt_id)
        
        # 参数设置
        self.params = {
            "boll_period": 20,           # Bollinger Bands 周期
            "boll_dev": 1,               # Bollinger Bands 带宽系数
            "atr_period": 14,            # ATR 周期
            "atr_multiplier": 2,         # ATR 止损倍数
            "stoploss": None,            # 固定止损
            "takeprofit": None,          # 固定止盈
        }
        
        # 变量初始化
        self.boll_up = 0.0              # Bollinger Bands 上轨
        self.boll_down = 0.0            # Bollinger Bands 下轨
        self.boll_mid = 0.0             # Bollinger Bands 中轨
        self.atr_value = 0.0            # ATR 值
        self.pos = 0                    # 当前持仓
        self.entry_price = 0.0          # 开仓价格
        self.in_trade = False           # 是否持仓中
        
        # 行情缓存
        self.bar: BarData = None
        self.bars_buffer = []           # K 线数据缓冲
        
    def on_init(self):
        """初始化策略"""
        self.write_log(f"策略初始化：{self.strategy_name}")
        self.write_log(f"参数：{self.params}")
        
    def on_start(self):
        """启动策略"""
        self.write_log("策略启动")
        self.bar = BarData()
        self.bars_buffer = []
        
    def on_stop(self):
        """停止策略"""
        self.write_log("策略停止")
        
    def on_tick(self, tick: TickData):
        """Tick 回调"""
        try:
            # 缓存 Tick 数据
            self.bar.last_price = tick.last_price
            self.bar.last_volume = 1
            self.bar.open_interest = tick.open_interest
            self.bar.high_price = tick.high_price
            self.bar.low_price = tick.low_price
            self.bar.bid_price = tick.bid_price
            self.bar.bid_volume = tick.bid_volume
            self.bar.ask_price = tick.ask_price
            self.bar.ask_volume = tick.ask_volume
            self.bar.datetime = tick.datetime
            
            # 更新 K 线
            self.bar.update()
            
            # 生成 K 线
            self.bg.update_current(self.bar)
            
        except Exception as e:
            self.write_log(f"Tick 处理错误：{e}")
            
    def on_bar(self, bar: BarData):
        """K 线回调"""
        try:
            self.bar = bar
            
            # 等待 K 线生成
            if not self.bar.is_inited:
                return
            
            # 缓存 K 线
            self.bars_buffer.append(bar)
            
            # 计算 Bollinger Bands
            self.calculate_boll()
            
            # 计算 ATR
            self.calculate_atr()
            
            # 处理信号
            self.handle_signal()
            
        except Exception as e:
            self.write_log(f"Bar 处理错误：{e}")
            
    def calculate_boll(self):
        """计算 Bollinger Bands"""
        boll = self.params["boll_period"]
        dev = self.params["boll_dev"]
        
        # 使用缓冲数据
        if len(self.bars_buffer) < boll:
            return
            
        # 获取最近 boll 条 K 线
        recent_bars = self.bars_buffer[-boll:]
        
        # 计算收盘价均值
        close_prices = [bar.close_price for bar in recent_bars]
        mid = np.mean(close_prices)
        
        # 计算标准差
        std = np.std(close_prices)
        
        # 计算上下轨
        self.boll_up = mid + std * dev
        self.boll_down = mid - std * dev
        self.boll_mid = mid
        
    def calculate_atr(self):
        """计算 ATR"""
        atr = self.params["atr_period"]
        
        # 获取最近 atr 条 K 线
        if len(self.bars_buffer) < atr:
            return
            
        recent_bars = self.bars_buffer[-atr:]
        
        # 计算真实波幅 (TR = max(high-low, |high-prev_low|, |low-prev_high|))
        tr_values = []
        for i, bar in enumerate(recent_bars):
            if i == 0:
                tr = max(bar.high_price - bar.low_price, 
                        abs(bar.high_price - recent_bars[-2].low_price),
                        abs(bar.low_price - recent_bars[-2].high_price))
            else:
                tr = max(bar.high_price - bar.low_price,
                        abs(bar.high_price - recent_bars[-2].low_price),
                        abs(bar.low_price - recent_bars[-2].high_price))
            tr_values.append(tr)
            
        atr_value = np.mean(tr_values)
        self.atr_value = atr_value
        
    def handle_signal(self):
        """处理交易信号"""
        try:
            # 获取当前价格
            current_price = self.bar.close_price
            
            # 检查持仓
            if self.pos == 0:
                # 空仓，判断是否开仓
                if current_price > self.boll_up:
                    # 突破上轨，开多
                    self.buy(1, current_price)
                    self.write_log(f"开多信号：价格{current_price:.2f} > 上轨{self.boll_up:.2f}")
                    self.entry_price = current_price
                    self.in_trade = True
                elif current_price < self.boll_down:
                    # 突破下轨，开空
                    self.short(1, current_price)
                    self.write_log(f"开空信号：价格{current_price:.2f} < 下轨{self.boll_down:.2f}")
                    self.entry_price = current_price
                    self.in_trade = True
            else:
                # 有持仓，判断是否平仓
                if self.pos > 0:
                    # 多单
                    stop_price = self.entry_price - self.atr_value * self.params["atr_multiplier"]
                    take_profit_price = self.entry_price + self.params["takeprofit"] if self.params["takeprofit"] else float('inf')
                    
                    if current_price <= stop_price:
                        # 触发止损
                        self.close_all()
                        self.write_log(f"多单止损：价格{current_price:.2f} <= 止损{stop_price:.2f}")
                    elif current_price >= take_profit_price:
                        # 触发止盈
                        self.close_all()
                        self.write_log(f"多单止盈：价格{current_price:.2f} >= 止盈{take_profit_price:.2f}")
                        
                else:
                    # 空单
                    stop_price = self.entry_price + self.atr_value * self.params["atr_multiplier"]
                    take_profit_price = self.entry_price - self.params["takeprofit"] if self.params["takeprofit"] else float('-inf')
                    
                    if current_price >= stop_price:
                        # 触发止损
                        self.close_all()
                        self.write_log(f"空单止损：价格{current_price:.2f} >= 止损{stop_price:.2f}")
                    elif current_price <= take_profit_price:
                        # 触发止盈
                        self.close_all()
                        self.write_log(f"空单止盈：价格{current_price:.2f} <= 止盈{take_profit_price:.2f}")
                        
        except Exception as e:
            self.write_log(f"信号处理错误：{e}")
            
    def on_corrupt(self):
        """数据损坏处理"""
        self.write_log("数据损坏，重置策略")
        self.bars_buffer = []
        self.boll_up = 0
        self.boll_down = 0
        self.boll_mid = 0
        self.atr_value = 0
        
    def on_history(self, bars):
        """历史数据回调"""
        self.write_log(f"加载历史数据：{len(bars)} 条")
        self.bars_buffer.extend(bars)
        
    def get_bars(self):
        """获取 K 线数据 - 修复版"""
        # 使用本地缓冲数据
        return self.bars_buffer


if __name__ == "__main__":
    # 测试示例
    print("CTA 趋势跟踪策略 - 修复版")
    print("策略参数:")
    print("- boll_period: 20")
    print("- boll_dev: 1")
    print("- atr_period: 14")
    print("- atr_multiplier: 2")
    print("- stoploss: None")
    print("- takeprofit: None")
