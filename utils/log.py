import logging

# 配置日志：输出到控制台，显示 DEBUG 级别以上日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

base_logger = logging.getLogger()
