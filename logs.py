import os
import logging


class Logs:

    logger = None
    console_handler = None

    def __init__(self):
        if Logs.logger is None:
            Logs.set()

    @staticmethod
    def set():
        os.environ["WDM_LOG_LEVEL"] = str(logging.ERROR)
        os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
        logFormatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
        Logs.logger = logging.getLogger(__name__)
        Logs.logger.setLevel(logging.DEBUG)
        Logs.console_handler = logging.StreamHandler()
        Logs.console_handler.setFormatter(logFormatter)
        Logs.logger.addHandler(Logs.console_handler)

    @staticmethod
    def terminate():
        logging.shutdown()

    @staticmethod
    def log_info(message):
        Logs.logger.info(message)

    @staticmethod
    def log_debug(message):
        Logs.logger.debug(message)

    @staticmethod
    def log_error(message):
        Logs.logger.error(message)

    @staticmethod
    def log_warning(message):
        Logs.logger.warning(message)

    @staticmethod
    def log_critical(message):
        Logs.logger.critical(message)
