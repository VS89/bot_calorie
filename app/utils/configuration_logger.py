import logging
from logging.handlers import TimedRotatingFileHandler


class ConfigurationLogger:

    @staticmethod
    def log_setup() -> logging.Logger:
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                                      datefmt='%d.%m.%Y %H:%M:%S')
        handler = TimedRotatingFileHandler(filename='.log_files/pohydizirui_tgbot_log.txt', when='midnight')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        return log


logger = ConfigurationLogger.log_setup()
