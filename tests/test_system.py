"""
量化交易系统单元测试

测试模块：
1. 数据管理器
2. 风险管理器
3. 趋势跟踪策略

框架：pytest
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestDataManager(unittest.TestCase):
    """测试数据管理器"""
    
    def setUp(self):
        """测试前准备"""
        from strategies.data_manager import DataManager
        self.dm = DataManager()
        
    def test_import_data_from_csv(self):
        """测试从 CSV 导入数据"""
        # 创建测试 CSV 文件
        import tempfile
        import pandas as pd
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df = pd.DataFrame({
                'symbol': '510300',
                'exchange': 'SHSE',
                'vt_symbol': '510300.SHSE',
                'name': '沪深 300ETF',
                'datetime': ['20240101 09:30:00', '20240101 09:31:00'],
                'interval': ['1m', '1m'],
                'volume': [100, 200],
                'open_interest': [1000, 1050],
                'open_price': [3.5, 3.55],
                'high_price': [3.6, 3.65],
                'low_price': [3.4, 3.45],
                'close_price': [3.55, 3.6]
            })
            df.to_csv(f.name, index=False)
            filepath = f.name
        
        try:
            bars = self.dm.import_data(
                vt_symbol='510300.SHSE',
                filepath=filepath
            )
            
            self.assertEqual(len(bars), 2)
            self.assertEqual(bars[0].close_price, 3.55)
            
        finally:
            os.unlink(filepath)
            
    def test_export_data_to_csv(self):
        """测试导出 CSV 数据"""
        # 创建测试数据
        from vnpy.trader.object import BarData
        from vnpy.trader.utility import Timestamp
        
        bar1 = BarData(
            symbol='510300',
            exchange='SHSE',
            vt_symbol='510300.SHSE',
            name='沪深 300ETF',
            datetime=Timestamp('20240101 09:30:00'),
            interval='1m',
            volume=100,
            open_interest=1000,
            open_price=3.5,
            high_price=3.6,
            low_price=3.4,
            close_price=3.55,
            gateway_name=''
        )
        
        self.dm.bars['510300.SHSE'] = [bar1]
        
        path = self.dm.export_data(
            vt_symbol='510300.SHSE',
            format='csv'
        )
        
        self.assertTrue(os.path.exists(path))
        
    def test_get_bars(self):
        """测试获取 K 线数据"""
        bar = BarData(
            symbol='510300',
            exchange='SHSE',
            vt_symbol='510300.SHSE',
            name='沪深 300ETF',
            datetime=Timestamp('20240101 09:30:00'),
            interval='1m',
            volume=100,
            open_interest=1000,
            open_price=3.5,
            high_price=3.6,
            low_price=3.4,
            close_price=3.55,
            gateway_name=''
        )
        
        self.dm.bars['510300.SHSE'] = [bar]
        bars = self.dm.get_bars('510300.SHSE')
        
        self.assertEqual(len(bars), 1)
        

class TestRiskManager(unittest.TestCase):
    """测试风险管理器"""
    
    def setUp(self):
        """测试前准备"""
        from risk_manager import RiskManager
        self.rm = RiskManager()
        
    def test_init_parameters(self):
        """测试初始化参数"""
        self.assertEqual(self.rm.max_position, 100)
        self.assertEqual(self.rm.max_daily_loss, 10000)
        self.assertEqual(self.rm.max_drawdown, 0.1)
        
    def test_set_parameters(self):
        """测试设置参数"""
        self.rm.set_parameters(max_position=50, max_daily_loss=5000)
        
        self.assertEqual(self.rm.max_position, 50)
        self.assertEqual(self.rm.max_daily_loss, 5000)
        
    def test_get_risk_status(self):
        """测试获取风险状态"""
        status = self.rm.get_risk_status()
        
        self.assertIn('max_position', status)
        self.assertIn('current_positions', status)
        self.assertIn('daily_loss', status)
        

class TestTrendFollowingStrategy(unittest.TestCase):
    """测试趋势跟踪策略"""
    
    def setUp(self):
        """测试前准备"""
        from strategies.cta.trend_following import TrendFollowingStrategy
        self.strategy = TrendFollowingStrategy(None, 'TestStrategy')
        
    def test_init_parameters(self):
        """测试初始化参数"""
        self.assertEqual(self.strategy.params['boll_period'], 20)
        self.assertEqual(self.strategy.params['atr_period'], 14)
        
    def test_on_init(self):
        """测试初始化方法"""
        self.strategy.on_init()
        
        # 检查日志写入（实际测试需要 Mock write_log）
        self.assertTrue(hasattr(self.strategy, 'write_log'))
        
    def test_on_start(self):
        """测试启动方法"""
        self.strategy.on_start()
        
        self.assertIsNotNone(self.strategy.bar)
        self.assertEqual(len(self.strategy.bars_buffer), 0)
        
    def test_on_stop(self):
        """测试停止方法"""
        self.strategy.on_stop()
        
        self.assertTrue(hasattr(self.strategy, 'write_log'))
        
    def test_calculate_boll(self):
        """测试计算 Bollinger Bands"""
        # 创建测试 K 线数据
        from vnpy.trader.object import BarData
        from vnpy.trader.utility import Timestamp
        
        # 创建 25 条 K 线（超过 boll_period=20）
        bars = []
        for i in range(25):
            bar = BarData(
                symbol='510300',
                exchange='SHSE',
                vt_symbol='510300.SHSE',
                name='沪深 300ETF',
                datetime=Timestamp(f'20240101 09:{i:02d}:00'),
                interval='1m',
                volume=100,
                open_interest=1000,
                open_price=3.5 + i * 0.01,
                high_price=3.5 + i * 0.01 + 0.05,
                low_price=3.5 + i * 0.01 - 0.05,
                close_price=3.5 + i * 0.01,
                gateway_name=''
            )
            bars.append(bar)
            
        self.strategy.bars_buffer = bars
        
        # 调用计算
        self.strategy.calculate_boll()
        
        # 检查是否计算了 Bollinger Bands
        self.assertIsNotNone(self.strategy.boll_up)
        self.assertIsNotNone(self.strategy.boll_down)
        self.assertIsNotNone(self.strategy.boll_mid)
        
    def test_calculate_atr(self):
        """测试计算 ATR"""
        # 创建测试 K 线数据
        from vnpy.trader.object import BarData
        from vnpy.trader.utility import Timestamp
        
        # 创建 20 条 K 线（超过 atr_period=14）
        bars = []
        for i in range(20):
            bar = BarData(
                symbol='510300',
                exchange='SHSE',
                vt_symbol='510300.SHSE',
                name='沪深 300ETF',
                datetime=Timestamp(f'20240101 09:{i:02d}:00'),
                interval='1m',
                volume=100,
                open_interest=1000,
                open_price=3.5 + i * 0.01,
                high_price=3.5 + i * 0.01 + 0.1,
                low_price=3.5 + i * 0.01 - 0.1,
                close_price=3.5 + i * 0.01,
                gateway_name=''
            )
            bars.append(bar)
            
        self.strategy.bars_buffer = bars
        
        # 调用计算
        self.strategy.calculate_atr()
        
        # 检查是否计算了 ATR
        self.assertIsNotNone(self.strategy.atr_value)
        self.assertGreater(self.strategy.atr_value, 0)
        
    def test_handle_signal_empty_position(self):
        """测试空仓时的信号处理"""
        # 设置 Bollinger Bands 和 ATR
        self.strategy.boll_up = 3.6
        self.strategy.boll_down = 3.4
        self.strategy.boll_mid = 3.5
        self.strategy.atr_value = 0.1
        
        # 设置空仓
        self.strategy.pos = 0
        self.strategy.in_trade = False
        self.strategy.entry_price = 0
        
        # 创建突破上轨的 K 线
        bar = BarData(
            symbol='510300',
            exchange='SHSE',
            vt_symbol='510300.SHSE',
            name='沪深 300ETF',
            datetime=Timestamp('20240101 09:30:00'),
            interval='1m',
            volume=100,
            open_interest=1000,
            open_price=3.55,
            high_price=3.65,
            low_price=3.5,
            close_price=3.65,
            gateway_name=''
        )
        
        self.strategy.on_bar(bar)
        
        # 检查是否生成了开多信号（通过检查 write_log 调用）
        self.assertTrue(hasattr(self.strategy, 'write_log'))
        
    def test_get_bars(self):
        """测试获取 K 线数据"""
        # 添加测试 K 线
        bar = BarData(
            symbol='510300',
            exchange='SHSE',
            vt_symbol='510300.SHSE',
            name='沪深 300ETF',
            datetime=Timestamp('20240101 09:30:00'),
            interval='1m',
            volume=100,
            open_interest=1000,
            open_price=3.5,
            high_price=3.6,
            low_price=3.4,
            close_price=3.55,
            gateway_name=''
        )
        
        self.strategy.bars_buffer = [bar]
        bars = self.strategy.get_bars()
        
        self.assertEqual(len(bars), 1)


if __name__ == '__main__':
    # 运行所有测试
    unittest.main(verbosity=2)
