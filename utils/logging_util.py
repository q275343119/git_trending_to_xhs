from loguru import logger
import os

from config import config_settings

# 获取项目根目录路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = config_settings.log_dir
LOG_FILE = os.path.join(BASE_DIR, os.path.join(LOG_DIR, config_settings.log_file))
LOG_LEVEL = config_settings.log_level
LOG_TO_CONSOLE = config_settings.log_to_console

# 获取项目根目录路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 确保日志文件路径存在
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# 移除 loguru 的默认配置
logger.remove()

# 配置文件日志输出
logger.add(
    LOG_FILE,
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    level=LOG_LEVEL,
    rotation="1 day",  # 按天轮转日志
    retention="7 days",  # 保留7天的日志
    backtrace=True,  # 捕捉完整的错误堆栈
    diagnose=True,  # 诊断错误细节
    encoding='utf-8'  # 文件编码
)

# 配置控制台日志输出
if LOG_TO_CONSOLE:
    logger.add(
        lambda msg: print(msg),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,  # 启用颜色
        level=LOG_LEVEL,
    )

# 示例：在当前模块内添加测试日志
if __name__ == "__main__":
    logger.debug("This is a debug message from logging_util.py")
    logger.info("This is an info message from logging_util.py")
    logger.warning("This is a warning message from logging_util.py")
    logger.error("This is an error message from logging_util.py")
    logger.critical("This is a critical message from logging_util.py")
