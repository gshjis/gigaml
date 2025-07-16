import logging
import logging.config
from pathlib import Path

def setup_logging():
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "default": {
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
            "file": {
                "formatter": "standard",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["default", "file"],
                "level": "ERROR",
                "propagate": False
            },
            "uvicorn": {
                "handlers": ["default", "file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.error": {
                "handlers": ["default", "file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.access": {
                "handlers": ["default", "file"],
                "level": "INFO",
                "propagate": False
            },
        }
    }

    logging.config.dictConfig(log_config)
    return logging.getLogger(__name__)

logger = setup_logging()
