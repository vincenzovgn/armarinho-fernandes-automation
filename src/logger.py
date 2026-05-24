import logging
import logging.config
from logging import Logger

from config import Config

config = Config()
LOGGING_CONFIG = {
  'version': 1,
  'formatters': {
    'simple': {
      'format': '%(asctime)s [%(process)d] [%(levelname)s] - %(message)s',
      'datefmt': '%Y-%m-%d'
    }
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'stream': 'ext://sys.stdout',
      'formatter': 'simple',
      'level': config.LOG_LEVEL
    }
  },
  'loggers': {
    'console': {
      'level': config.LOG_LEVEL,
      'handlers': ['console'],
      'propagete': False
    }
  },
  'root': {
    'level': 'DEBUG',
    'handlers': ['console']
  }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger: Logger = logging.getLogger(__name__)