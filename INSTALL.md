# 安装指南

## 1. 环境准备

### 1.1 Python 安装

```bash
# 下载 Python 3.10+
https://www.python.org/downloads/

# 或安装 VeighNa Studio（推荐）
https://download.vnpy.com/veighna_studio-4.3.0.exe
```

### 1.2 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

## 2. 安装依赖

### 2.1 核心依赖

```bash
pip install vnpy==4.3.0
pip install vnpy_ctp==1.0.0
pip install vnpy_ctastrategy==1.0.0
pip install vnpy_ctabacktester==1.0.0
pip install vnpy_datamanager==1.0.0
pip install vnpy_riskmanager==1.0.0
pip install vnpy_webtrader==1.0.0
pip install vnpy_chartwizard==1.0.0
```

### 2.2 数据库依赖

```bash
pip install pymysql==1.0.0
pip install psycopg2==2.8.0
pip install aiomysql==0.2.0
pip install asyncpg==0.23.0
```

### 2.3 数据处理

```bash
pip install pandas==1.5.0
pip install numpy==1.21.0
```

### 2.4 可视化

```bash
pip install matplotlib==3.5.0
pip install pyqt5==5.15.0
pip install pyqtwebengine==5.15.0
```

### 2.5 数据服务（可选）

```bash
pip install rqdata==2.0.0
pip install tushare==1.2.89
```

## 3. 安装交易接口

### 3.1 CTP 接口（A 股、ETF 期权）

```bash
pip install vnpy_ctp==1.0.0
```

### 3.2 XTP 接口（A 股、ETF 期权）

```bash
pip install vnpy_xtp==1.0.0
```

### 3.3 华鑫奇点接口

```bash
pip install vnpy_tora==1.0.0
```

### 3.4 东方财富 EMT 接口

```bash
pip install vnpy_emt==1.0.0
```

### 3.5 掘金接口

```bash
pip install vnpy_gm==1.0.0
```

## 4. 配置交易接口

### 4.1 CTP 配置

编辑 `config/gateway.py`：

```python
from vnpy.trader.setting import SETTINGS

SETTINGS["gateway.1.name"] = "CTP"
SETTINGS["gateway.1.type"] = "CTP"
SETTINGS["gateway.1.password"] = ""
SETTINGS["gateway.1.brokerid"] = "9999"  # 经纪商代码
SETTINGS["gateway.1.userid"] = ""
SETTINGS["gateway.1.appid"] = ""
SETTINGS["gateway.1.authcode"] = ""
SETTINGS["gateway.1.product"] = "CFFEX"
SETTINGS["gateway.1.variety"] = "CTP"
```

### 4.2 获取 CTP 配置

1. 访问 [SimNow](http://www.simnow.com.cn/)
2. 注册账号并获取配置信息
3. 配置信息：
   - 经纪商代码：9999
   - 交易服务器：180.131.4.148:10203
   - 行情服务器：180.131.4.148:10211
   - 授权文件路径：`D:\SimNow\ctp\authfile`

### 4.3 XTP 配置

```python
SETTINGS["gateway.2.name"] = "XTP"
SETTINGS["gateway.2.type"] = "XTP"
SETTINGS["gateway.2.password"] = ""
SETTINGS["gateway.2.user"] = ""
SETTINGS["gateway.2.secret"] = ""
SETTINGS["gateway.2.host"] = "101.37.130.100"
SETTINGS["gateway.2.port"] = "443"
```

## 5. 安装数据服务

### 5.1 RQData（推荐）

```bash
pip install rqdata==2.0.0

# 登录 RQData
rqdata login your_email
```

### 5.2 TuShare

```bash
pip install tushare==1.2.89

# 设置 API 密钥
export TUSHARE_TOKEN="your_token"
```

### 5.3 迅投研

```bash
# 下载迅投研客户端
# https://www.xtstudy.com/
```

## 6. 数据库安装

### 6.1 SQLite（默认）

无需安装，Python 标准库自带。

### 6.2 MySQL

```bash
# 下载 MySQL
https://dev.mysql.com/downloads/

# 安装 Python 驱动
pip install pymysql
```

### 6.3 PostgreSQL

```bash
# 下载 PostgreSQL
https://www.postgresql.org/download/

# 安装 Python 驱动
pip install psycopg2
```

## 7. 验证安装

```bash
# 检查 Python 版本
python --version

# 检查 VeighNa
python -c "import vnpy; print(vnpy.__version__)"

# 检查交易接口
python -c "import vnpy_ctp; print('CTP 接口已安装')"

# 检查策略模块
python -c "import vnpy_ctastrategy; print('CTA 策略模块已安装')"

# 检查数据管理
python -c "import vnpy_datamanager; print('数据管理模块已安装')"
```

## 8. 常见问题

### 8.1 依赖冲突

```bash
# 使用 pip-tools 管理依赖
pip install pip-tools
pip-compile requirements.in
```

### 8.2 权限问题

```bash
# Windows
pip install --user -r requirements.txt

# Linux/Mac
sudo pip install -r requirements.txt
```

### 8.3 网络问题

```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 9. 下一步

1. 配置交易接口
2. 导入历史数据
3. 编写策略代码
4. 运行回测
5. 实盘交易
