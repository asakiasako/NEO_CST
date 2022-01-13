import logging
import os.path
from logging import Formatter, handlers, root, DEBUG, WARNING, FileHandler, getLogger
from paths import get_sub_dir

# Configure root logger
def configure_logger():
    configure_root_logger()
    configure_loop_test_logger()


def configure_root_logger(level=WARNING, echo=True):
    # === root ===
    ROOT_LOG_PATH = os.path.join(get_sub_dir('Logs'), 'RPC-Server-LOG')
    root.setLevel(level)

    fmt = Formatter(fmt='\n[%(asctime)s] %(name)s - %(levelname)s - %(message)s')

    file_handler = handlers.TimedRotatingFileHandler(ROOT_LOG_PATH, when='D', backupCount=14)
    console_handler = logging.StreamHandler()
    file_handler.setFormatter(fmt)
    console_handler.setFormatter(fmt)

    root.addHandler(file_handler)
    if echo:
        root.addHandler(console_handler)


def configure_loop_test_logger(level=DEBUG):
    # === running-test ===
    TEST_LOG_PATH = os.path.join(get_sub_dir('Logs'), 'LoopTest.log')
    logger = getLogger('LoopTest')
    logger.setLevel(level)

    fmt = Formatter(fmt='\n[%(asctime)s] %(name)s - %(levelname)s - %(message)s')

    file_handler = FileHandler(TEST_LOG_PATH, 'w')
    file_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
