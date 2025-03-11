import json
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class JSONFormatter(logging.Formatter):
    def __init__(self, instance):
        self.instance = instance
        super().__init__()

    def format(self, record):
        log_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "level": record.levelname,
            "instance": self.instance,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_record["stack_trace"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logger(name, log_dir="./logs", log_level=logging.DEBUG):
    logger_ = logging.getLogger(name)
    logger_.setLevel(log_level)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f"{name}.log")
    file_handler = RotatingFileHandler(
        log_file, maxBytes=2 * 1024 * 1024, backupCount=30
    )
    file_handler.setLevel(log_level)

    formatter = JSONFormatter(name)
    file_handler.setFormatter(formatter)

    logger_.addHandler(file_handler)

    return logger_


logger = setup_logger("bot")
