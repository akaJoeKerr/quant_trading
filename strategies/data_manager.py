"""
数据管理模块（增强版）

用于管理 A 股和 ETF 期权的 historical data

**优化说明 (2026-03-25):**
- 添加错误处理和日志记录
- 支持 Parquet/HDF5 格式
- 添加数据验证
- 集成 VeighNa 数据库层（预留接口）
"""

from vnpy.trader.object import BarData, TickData
from vnpy.trader.utility import IntervalType, Timestamp
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import os
import logging


# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataManager:
    """
    数据管理器（增强版）
    
    功能：
    1. 导入历史数据
    2. 管理数据文件
    3. 查询历史数据
    4. 导出数据文件
    5. 数据验证
    6. 数据库集成（预留接口）
    """
    
    def __init__(self, data_path="./data"):
        """初始化数据管理器"""
        self.bars: dict = {}  # K 线数据缓存
        self.ticks: dict = {}  # Tick 数据缓存
        self.data_path = data_path  # 数据存储路径
        self.db_manager = None  # 数据库管理器（预留）
        
        # 确保数据目录存在
        os.makedirs(self.data_path, exist_ok=True)
        logger.info(f"数据管理器初始化完成，数据路径：{self.data_path}")
        
    def import_data(
        self,
        vt_symbol: str,
        interval: str = "1m",
        start: str = "20200101",
        end: str = "20240325",
        filepath: str = None,
        format: str = "csv"  # csv / parquet / hdf5
    ) -> list:
        """
        导入历史数据（增强版）
        
        参数：
        - vt_symbol: 合约代码，如"510300.SHSE"
        - interval: K 线周期，如"1m", "5m", "1h"
        - start: 开始日期，格式"YYYYMMDD"
        - end: 结束日期，格式"YYYYMMDD"
        - filepath: 数据文件路径，None 则自动查找
        - format: 文件格式，默认 csv
        
        返回：
        - BarData 列表
        
        异常：
        - FileNotFoundError: 文件不存在
        - ValueError: 文件格式错误
        """
        try:
            # 生成数据文件名
            filename = f"{vt_symbol}_{interval}.{format}"
            
            # 确定文件路径
            if filepath is None:
                path = os.path.join(self.data_path, filename)
            else:
                path = filepath
            
            # 检查文件是否存在
            if not os.path.exists(path):
                raise FileNotFoundError(f"数据文件不存在：{path}")
            
            # 读取数据
            bars = self._read_data(path, format)
            
            # 验证数据
            if not self._validate_bars(bars):
                logger.warning(f"数据验证失败：{vt_symbol}")
                return []
                
            # 缓存数据
            self.bars[vt_symbol] = bars
            logger.info(f"成功导入数据：{vt_symbol}, 共{len(bars)}条")
            
            return bars
            
        except FileNotFoundError as e:
            logger.error(f"文件不存在：{e}")
            return []
        except Exception as e:
            logger.error(f"导入数据错误：{e}")
            return []
            
    def _read_data(self, path: str, format: str) -> list:
        """读取数据文件"""
        if format == "csv":
            return self._read_csv(path)
        elif format == "parquet":
            return self._read_parquet(path)
        elif format == "hdf5":
            return self._read_hdf5(path)
        else:
            raise ValueError(f"不支持的文件格式：{format}")
            
    def _read_csv(self, path: str) -> list:
        """读取 CSV 数据"""
        try:
            df = pd.read_csv(path)
            return [self._bar_from_row(row) for _, row in df.iterrows()]
        except Exception as e:
            logger.error(f"CSV 读取错误：{e}")
            raise
            
    def _read_parquet(self, path: str) -> list:
        """读取 Parquet 数据"""
        try:
            df = pd.read_parquet(path)
            return [self._bar_from_row(row) for _, row in df.iterrows()]
        except Exception as e:
            logger.error(f"Parquet 读取错误：{e}")
            raise
            
    def _read_hdf5(self, path: str) -> list:
        """读取 HDF5 数据"""
        try:
            df = pd.read_hdf(path)
            return [self._bar_from_row(row) for _, row in df.iterrows()]
        except Exception as e:
            logger.error(f"HDF5 读取错误：{e}")
            raise
            
    def _bar_from_row(self, row: pd.Series) -> BarData:
        """从 CSV 行创建 BarData 对象"""
        return BarData(
            symbol=row.get("symbol", ""),
            exchange=row.get("exchange", ""),
            vt_symbol=row.get("vt_symbol", ""),
            name=row.get("name", ""),
            datetime=Timestamp(row.get("datetime", "")),
            interval=row.get("interval", ""),
            volume=row.get("volume", 0),
            open_interest=row.get("open_interest", 0),
            open_price=row.get("open_price", 0),
            high_price=row.get("high_price", 0),
            low_price=row.get("low_price", 0),
            close_price=row.get("close_price", 0),
            gateway_name=""
        )
        
    def _validate_bars(self, bars: list) -> bool:
        """验证数据"""
        if not bars:
            logger.warning("数据为空")
            return False
            
        # 检查时间顺序
        for i in range(1, len(bars)):
            if bars[i].datetime <= bars[i-1].datetime:
                logger.warning(f"时间顺序错误：{bars[i].datetime} <= {bars[i-1].datetime}")
                return False
                
        # 检查价格合理性
        for bar in bars:
            if bar.high_price < bar.low_price:
                logger.warning(f"价格异常：{bar}")
                return False
                
        return True
        
    def export_data(
        self,
        vt_symbol: str,
        interval: str = "1m",
        start: str = "20200101",
        end: str = "20240325",
        filepath: str = None,
        format: str = "csv"
    ) -> str:
        """
        导出数据到文件
        
        参数：
        - vt_symbol: 合约代码
        - interval: K 线周期
        - start: 开始日期
        - end: 结束日期
        - filepath: 输出文件路径
        - format: 文件格式
        
        返回：
        - 文件路径
        """
        try:
            # 生成文件名
            filename = f"{vt_symbol}_{interval}.{format}"
            
            # 确定文件路径
            if filepath is None:
                path = os.path.join(self.data_path, filename)
            else:
                path = filepath
            
            # 确保目录存在
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
            
            # 获取数据
            bars = self.bars.get(vt_symbol, [])
            
            # 导出到文件
            if bars:
                if format == "csv":
                    self._export_csv(bars, path)
                elif format == "parquet":
                    self._export_parquet(bars, path)
                elif format == "hdf5":
                    self._export_hdf5(bars, path)
                else:
                    raise ValueError(f"不支持的导出格式：{format}")
                
                logger.info(f"成功导出数据到：{path}")
                return path
            else:
                logger.warning(f"无数据可导出：{vt_symbol}")
                return None
                
        except Exception as e:
            logger.error(f"导出数据错误：{e}")
            return None
            
    def _export_csv(self, bars: list, path: str):
        """导出到 CSV"""
        df = pd.DataFrame([self._row_from_bar(bar) for bar in bars])
        df.to_csv(path, index=False)
        
    def _export_parquet(self, bars: list, path: str):
        """导出到 Parquet"""
        df = pd.DataFrame([self._row_from_bar(bar) for bar in bars])
        df.to_parquet(path)
        
    def _export_hdf5(self, bars: list, path: str):
        """导出到 HDF5"""
        df = pd.DataFrame([self._row_from_bar(bar) for bar in bars])
        df.to_hdf(path, key=f"{bars[0].vt_symbol if bars else 'data'}", mode='w')
        
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
        logger.info("缓存数据已清空")
        
    # === 数据库集成预留接口 ===
    
    def init_database(self, db_type: str = "sqlite", db_path: str = "./data.db"):
        """初始化数据库连接"""
        try:
            from vnpy.database import DatabaseManager
            self.db_manager = DatabaseManager(db_type, db_path)
            logger.info(f"数据库连接初始化成功：{db_type}")
            return True
        except Exception as e:
            logger.error(f"数据库初始化失败：{e}")
            return False
            
    def save_to_database(self, vt_symbol: str, bars: list):
        """保存数据到数据库"""
        if not self.db_manager:
            logger.warning("数据库未初始化")
            return False
            
        try:
            self.db_manager.save_bars(vt_symbol, bars)
            logger.info(f"数据已保存到数据库：{vt_symbol}")
            return True
        except Exception as e:
            logger.error(f"保存数据库错误：{e}")
            return False
            
    def load_from_database(self, vt_symbol: str, start: str, end: str) -> list:
        """从数据库加载数据"""
        if not self.db_manager:
            logger.warning("数据库未初始化")
            return []
            
        try:
            bars = self.db_manager.load_bars(vt_symbol, start, end)
            logger.info(f"从数据库加载数据：{vt_symbol}, 共{len(bars)}条")
            return bars
        except Exception as e:
            logger.error(f"加载数据库错误：{e}")
            return []
            
    def sync_database_and_file(self, vt_symbol: str):
        """同步数据库和文件"""
        if not self.db_manager:
            logger.warning("数据库未初始化")
            return
            
        try:
            # 从数据库加载
            bars_db = self.load_from_database(vt_symbol, "20200101", "20240325")
            
            # 保存到文件
            self.export_data(vt_symbol, format="csv")
            
            # 更新缓存
            self.bars[vt_symbol] = bars_db
            
            logger.info(f"数据同步完成：{vt_symbol}")
        except Exception as e:
            logger.error(f"数据同步错误：{e}")


if __name__ == "__main__":
    # 测试示例
    print("数据管理器（增强版）测试")
    
    # 创建数据管理器
    dm = DataManager()
    
    # 导入数据
    try:
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
        
    except Exception as e:
        print(f"测试失败：{e}")
