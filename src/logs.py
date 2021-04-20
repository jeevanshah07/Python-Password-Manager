import logging
import sys

FORMAT = '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(funcName)s:%(message)s'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(format=FORMAT)

output_file_handler = logging.FileHandler("logs/log.log")
stdout_handler = logging.StreamHandler(sys.stdout)

logger.addHandler(output_file_handler)
logger.addHandler(stdout_handler)


def log_debug(message: str):
    return logger.debug(message)
