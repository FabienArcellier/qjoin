import logging


def debug(msg: str, logger_name: str = 'qjoin'):
    logger = _logger(logger_name)
    logger.debug(msg)


def warning(msg: str, logger_name: str = 'qjoin'):
    logger = _logger(logger_name)
    logger.warning(msg)


def _logger(logger_name: str = 'qjoin') -> logging.Logger:
    return logging.getLogger(logger_name)
