from vnpy.trader.setting import SETTINGS

# 交易接口设置
SETTINGS["gateway.1.name"] = "CTP"
SETTINGS["gateway.1.type"] = "CTP"
SETTINGS["gateway.1.password"] = ""
SETTINGS["gateway.1.brokerid"] = "9999"  # 经纪商代码
SETTINGS["gateway.1.userid"] = ""
SETTINGS["gateway.1.appid"] = ""
SETTINGS["gateway.1.authcode"] = ""
SETTINGS["gateway.1.product"] = "CFFEX"  # 股指期货
SETTINGS["gateway.1.variety"] = "CTP"    # 期货

# 数据库设置
SETTINGS["database"] = "sqlite"
SETTINGS["database.path"] = "./data.db"

# 日志设置
SETTINGS["log.active"] = True
SETTINGS["log.file"] = True
SETTINGS["log.file_name"] = "log"
SETTINGS["log.file_path"] = "./logs"
SETTINGS["log.file_size"] = 10485760
SETTINGS["log.max_files"] = 10
SETTINGS["log.datetime_format"] = "%Y-%m-%d %H:%M:%S"
SETTINGS["log.level"] = "INFO"
SETTINGS["log.time"] = True

# 邮件设置（可选）
SETTINGS["email.server"] = ""
SETTINGS["email.port"] = 25
SETTINGS["email.username"] = ""
SETTINGS["email.password"] = ""
SETTINGS["email.sender"] = ""
SETTINGS["email.receiver"] = ""

# 交易员设置
SETTINGS["trader.name"] = ""
SETTINGS["trader.dir"] = "./trader"
SETTINGS["trader.web"] = ""
SETTINGS["trader.ui"] = "qt"
SETTINGS["trader.setting"] = "setting.json"
SETTINGS["trader.log"] = "log.json"
SETTINGS["trader.error"] = "error.log"
SETTINGS["trader.app"] = "app.json"
SETTINGS["trader.gateway"] = "gateway.json"
SETTINGS["trader.database"] = "database.json"
SETTINGS["trader.datafeed"] = "datafeed.json"
SETTINGS["trader.risk"] = "risk.json"
SETTINGS["trader.web"] = "web.json"
SETTINGS["trader.ui"] = "ui.json"
SETTINGS["trader.rpc"] = "rpc.json"
SETTINGS["trader.chart"] = "chart.json"
SETTINGS["trader.data"] = "data.json"
