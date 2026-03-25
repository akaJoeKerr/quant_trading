# VeighNa 事件驱动引擎

事件驱动引擎是量化交易系统的核心组件，负责管理事件的生产、分发和处理。

## 核心概念

### Event（事件）

事件是事件驱动架构中的基本单元，包含：

- **type**: 事件类型（如 EVENT_TICK, EVENT_ORDER）
- **data**: 事件数据（如 TickData, OrderData）

### EventEngine（事件引擎）

事件引擎负责：

1. **事件注册**: 注册事件处理器
2. **事件分发**: 将事件分发给对应的处理器
3. **事件管理**: 管理事件队列和处理器

## 事件类型

```python
EVENT_TICK      = "e.Tick"           # Tick 数据事件
EVENT_ORDER     = "e.Order"          # 委托事件
EVENT_TRADE     = "e.Trade"          # 成交事件
EVENT_POSITION  = "e.Position"       # 持仓事件
EVENT_ACCOUNT   = "e.Account"        # 资金事件
EVENT_CONTRACT  = "e.Contract"      # 合约事件
EVENT_LOG       = "e.Log"            # 日志事件
EVENT_QUOTE     = "e.Quote"         # 报价事件
```

## 使用示例

```python
from vnpy.event import Event, EventEngine
from vnpy.trader.event import EVENT_TICK
from vnpy.trader.object import TickData

# 创建事件引擎
event_engine = EventEngine()
event_engine.start()

# 注册事件处理器
def process_tick(event: Event):
    if event.type is EVENT_TICK:
        tick: TickData = event.data
        print(f"Tick: {tick}")

event_engine.register(EVENT_TICK, process_tick)

# 发送 Tick 事件
tick = TickData(symbol="SHFE.Cu", exchange="SHFE", ...)
event = Event(EVENT_TICK, tick)
event_engine.put(event)
```

## 事件处理器注册

```python
event_engine.register(event_type, handler)
```

- **event_type**: 事件类型字符串（如 EVENT_TICK）
- **handler**: 事件处理器函数

## 事件发送

```python
event_engine.put(event)
```

事件会被分发给所有注册了该类型事件的处理器。

## 事件引擎管理

```python
# 启动引擎
event_engine.start()

# 停止引擎
event_engine.stop()

# 关闭引擎
event_engine.close()
```

## 事件队列

事件引擎内部使用队列管理事件：

```python
from queue import Empty, Queue

self.queue: Queue = Queue()
```

事件以 FIFO 方式处理。

## 线程安全

事件引擎是线程安全的，支持多线程并发：

- **生产者线程**: 发送事件
- **消费者线程**: 处理事件

```python
self.thread = Thread(target=self.run)
self.thread.start()
```

## 事件数据

事件数据可以是任意对象，通常使用数据对象：

```python
class TickData:
    symbol: str
    exchange: str
    vt_symbol: str
    name: str
    last_price: float
    last_volume: int
    ...

event = Event(EVENT_TICK, tick_data)
```

## 事件类型管理

事件类型使用字符串标识，避免冲突：

```python
event_type = "e.Tick"  # 唯一标识
```

## 事件优先级

事件引擎按注册顺序处理事件，不支持优先级设置。

## 事件过滤

可以在事件处理器中实现事件过滤：

```python
def process_tick(event: Event):
    if event.type is not EVENT_TICK:
        return
    
    tick = event.data
    # 处理逻辑
```

## 事件日志

可以记录事件处理日志：

```python
def process_tick(event: Event):
    tick = event.data
    logger.info(f"收到 Tick 事件：{tick.vt_symbol}")
```

## 事件统计

可以统计事件数量：

```python
class TickEventStats:
    def __init__(self):
        self.count = 0
    
    def on_tick(self):
        self.count += 1
```

## 事件驱动优势

1. **解耦**: 生产者和消费者解耦
2. **异步**: 非阻塞式处理
3. **扩展**: 易于添加新事件类型
4. **并发**: 支持多线程处理

## 性能优化

1. **事件池**: 使用对象池减少创建开销
2. **批量处理**: 批量处理相似事件
3. **缓存**: 缓存常用数据

## 错误处理

事件处理器应处理异常：

```python
def process_tick(event: Event):
    try:
        # 处理逻辑
    except Exception as e:
        logger.error(f"事件处理错误：{e}")
```

## 最佳实践

1. **事件类型唯一**: 使用唯一的事件类型字符串
2. **数据对象**: 使用标准数据对象
3. **异常处理**: 处理事件处理异常
4. **日志记录**: 记录事件处理日志
5. **资源释放**: 及时释放事件引擎资源
