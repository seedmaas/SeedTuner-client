import logging
import os
from logging.handlers import TimedRotatingFileHandler


def init_logger():
    log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.log')
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # 创建 RotatingFileHandler 处理器实例，输出到文件中
    file_log_handler = TimedRotatingFileHandler(log_path, when='midnight', interval=1, backupCount=10)
    # file_log_handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=10, encoding='utf-8')
    file_log_handler.setFormatter(log_formatter)

    # 创建 StreamHandler 处理器实例，输出到控制台
    console_log_handler = logging.StreamHandler()
    console_log_handler.setFormatter(log_formatter)

    logger = logging.getLogger()
    # 检查当前环境变量，如果是生产环境，则不输出日志到控制台
    if os.environ.get('ENV') != 'production':
        # 为根日志处理器添加新的 StreamHandler 处理器，输出到控制台
        logger.addHandler(console_log_handler)
        logger.addHandler(file_log_handler)
        logger.setLevel(logging.DEBUG)
    else:
        logger.addHandler(file_log_handler)
        logger.setLevel(logging.INFO)
