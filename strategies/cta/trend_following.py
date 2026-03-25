"""
CTA 趋势跟踪策略示例

适用于 A 股和 ETF 期权的趋势跟踪策略
"""

from vnpy.trader.object import TickData, BarData
from vnpy.trader.strategy import StrategyTemplate
from vnpy.trader.utility import BarGenerator, ArrayTool
from vnpy.ctastrategy import CtaStrategyTemplate


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
        
        # 行情缓存
        self.bar: BarData = None
        
    def on_init(self):
        """初始化策略"""
        self.write_log(f"策略初始化：{self.strategy_name}")
        self.write_log(f"参数：{self.params}")
        
    def on_start(self):
        """启动策略"""
        self.write_log("策略启动")
        self.bar = BarData()
        
    def on_stop(self):
        """停止策略"""
        self.write_log("策略停止")
        
    def on_tick(self, tick: TickData):
        """Tick 回调"""
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
        
    def on_bar(self, bar: BarData):
        """K 线回调"""
        self.bar = bar
        
        # 等待 K 线生成
        if not self.bar.is_inited:
            return
        
        # 计算 Bollinger Bands
        self.calculate_boll()
        
        # 计算 ATR
        self.calculate_atr()
        
        # 处理信号
        self.handle_signal()
        
    def calculate_boll(self):
        """计算 Bollinger Bands"""
        boll = self.boll_period
        dev = self.params["boll_dev"]
        
        # 获取 K 线数据
        bars = self.get_bars()
        
        if len(bars) < boll:
            return
        
        # 计算收盘价均值
        close_prices = ArrayTool.extract_close(bars)
        mid = ArrayTool.rolling_mean(close_prices[-boll:], boll)
        
        # 计算标准差
        std = ArrayTool.rolling_std(close_prices[-boll:], boll)
        
        # 计算上下轨
        self.boll_up = mid + std * dev
        self.boll_down = mid - std * dev
        self.boll_mid = mid
        
    def calculate_atr(self):
        """计算 ATR"""
        atr = self.params["atr_period"]
        
        # 获取 K 线数据
        bars = self.get_bars()
        
        if len(bars) < atr:
            return
        
        # 计算真实波幅
        tr_values = ArrayTool.extract_tr(bars)
        atr_value = ArrayTool.rolling_mean(tr_values[-atr:], atr)
        
        self.atr_value = atr_value
        
    def handle_signal(self):
        """处理交易信号"""
        # 获取当前价格
        current_price = self.bar.close_price
        
        # 检查持仓
        if self.pos == 0:
            # 空仓，判断是否开仓
            if current_price > self.boll_up:
                # 突破上轨，开多
                self.buy()
                self.write_log(f"开多信号：价格{current_price} > 上轨{self.boll_up}")
            elif current_price < self.boll_down:
                # 突破下轨，开空
                self.short()
                self.write_log(f"开空信号：价格{current_price} < 下轨{self.boll_down}")
        else:
            # 有持仓，判断是否平仓
            if self.pos > 0:
                # 多单
                stop_price = self.entry_price - self.atr_value * self.params["atr_multiplier"]
                take_profit_price = self.entry_price + self.params["takeprofit"]
                
                if current_price <= stop_price:
                    # 触发止损
                    self.close_all()
                    self.write_log(f"多单止损：价格{current_price} <= 止损{stop_price}")
                elif current_price >= take_profit_price:
                    # 触发止盈
                    self.close_all()
                    self.write_log(f"多单止盈：价格{current_price} >= 止盈{take_profit_price}")
                    
            else:
                # 空单
                stop_price = self.entry_price + self.atr_value * self.params["atr_multiplier"]
                take_profit_price = self.entry_price - self.params["takeprofit"]
                
                if current_price >= stop_price:
                    # 触发止损
                    self.close_all()
                    self.write_log(f"空单止损：价格{current_price} >= 止损{stop_price}")
                elif current_price <= take_profit_price:
                    # 触发止盈
                    self.close_all()
                    self.write_log(f"空单止盈：价格{current_price} <= 止盈{take_profit_price}")
    
    def get_bars(self):
        """获取 K 线数据"""
        # 从策略引擎获取 K 线数据
        return self.strategy_engine.bars


if __name__ == "__main__":
    # 测试示例
    print("CTA 趋势跟踪策略示例")
    print("策略参数:")
    print("- boll_period: 20")
    print("- boll_dev: 1")
    print("- atr_period: 14")
    print("- atr_multiplier: 2")
    print("- stoploss: None")
    print("- takeprofit: None")
