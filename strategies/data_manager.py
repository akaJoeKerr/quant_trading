"""
数据管理模块

用于管理 A 股和 ETF 期权的 historical data
"""

from vnpy.trader.object import BarData, TickData
from vnpy.trader.utility import IntervalType, Timestamp
from datetime import datetime, timedelta
import pandas as pd
import os


class DataManager:
    """
    数据管理器
    
    功能：
    1. 导入历史数据
    2. 管理数据文件
    3. 查询历史数据
    4. 导出数据文件
    """
    
    def __init__(self):
        """初始化数据管理器"""
        self.bars: dict = {}  # K 线数据缓存
        self.ticks: dict = {}  # Tick 数据缓存
        self.data_path = "./data"  # 数据存储路径
        
    def import_data(
        self,
        vt_symbol: str,
        interval: str = "1m",
        start: str = "20200101",
        end: str = "20240325",
        filepath: str = None
    ) -> list:
        """
        导入历史数据
        
        参数：
        - vt_symbol: 合约代码，如"510300.SHSE"
        - interval: K 线周期，如"1m", "5m", "1h"
        - start: 开始日期，格式"YYYYMMDD"
        - end: 结束日期，格式"YYYYMMDD"
        - filepath: 数据文件路径，None 则自动查找
        
        返回：
        - BarData 列表
        """
        # 生成数据文件名
        filename = f"{vt_symbol}_{interval}.csv"
        
        # 确定文件路径
        if filepath is None:
            path = os.path.join(self.data_path, filename)
        else:
            path = filepath
        
        # 读取 CSV 数据
        bars = []
        if os.path.exists(path):
            df = pd.read_csv(path)
            bars = [self._bar_from_row(row) for _, row in df.iterrows()]
        
        # 缓存数据
        self.bars[vt_symbol] = bars
        
        return bars
    
    def _bar_from_row(self, row: pd.Series) -> BarData:
        """从 CSV 行创建 BarData 对象"""
        return BarData(
            symbol=row["symbol"],
            exchange=row["exchange"],
            vt_symbol=row["vt_symbol"],
            name=row["name"],
            datetime=Timestamp(row["datetime"]),
            interval=row["interval"],
            volume=row["volume"],
            open_interest=row["open_interest"],
            open_price=row["open_price"],
            high_price=row["high_price"],
            low_price=row["low_price"],
            close_price=row["close_price"],
            gateway_name=""
        )
    
    def export_data(
        self,
        vt_symbol: str,
        interval: str = "1m",
        start: str = "20200101",
        end: str = "20240325",
        filepath: str = None
    ) -> str:
        """
        导出数据到 CSV 文件
        
        参数：
        - vt_symbol: 合约代码
        - interval: K 线周期
        - start: 开始日期
        - end: 结束日期
        - filepath: 输出文件路径
        
        返回：
        - 文件路径
        """
        # 生成文件名
        filename = f"{vt_symbol}_{interval}.csv"
        
        # 确定文件路径
        if filepath is None:
            path = os.path.join(self.data_path, filename)
        else:
            path = filepath
        
        # 确保目录存在
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # 获取数据
        bars = self.bars.get(vt_symbol, [])
        
        # 导出到 CSV
        if bars:
            df = pd.DataFrame([self._row_from_bar(bar) for bar in bars])
            df.to_csv(path, index=False)
        
        return path
    
    def _row_from_bar(self, bar: BarData) -> pd.Series:
        """从 BarData 创建 CSV 行"""
        return pd.Series({
            "symbol": bar.symbol,
            "exchange": bar.exchange,
            "vt_symbol": bar.vt_symbol,
            "name": bar.name,
            "datetime": bar.datetime,
            "interval": bar.interval,
            "volume": bar.volume,
            "open_interest": bar.open_interest,
            "open_price": bar.open_price,
            "high_price": bar.high_price,
            "low_price": bar.low_price,
            "close_price": bar.close_price,
        })
    
    def get_bars(self, vt_symbol: str) -> list:
        """获取 K 线数据"""
        return self.bars.get(vt_symbol, [])
    
    def get_tick(self, vt_symbol: str) -> TickData:
        """获取最新 Tick 数据"""
        return self.ticks.get(vt_symbol)
    
    def set_tick(self, vt_symbol: str, tick: TickData):
        """设置 Tick 数据"""
        self.ticks[vt_symbol] = tick
    
    def clear_data(self):
        """清空缓存数据"""
        self.bars.clear()
        self.ticks.clear()


if __name__ == "__main__":
    # 测试示例
    dm = DataManager()
    
    # 导入数据
    bars = dm.import_data(
        vt_symbol="510300.SHSE",
        interval="1m",
        start="20240101",
        end="20240325"
    )
    
    print(f"导入数据条数：{len(bars)}")
    
    # 导出数据
    path = dm.export_data(
        vt_symbol="510300.SHSE",
        interval="1m",
        start="20240101",
        end="20240325"
    )
    
    print(f"导出数据到：{path}")
