import logging
import logging.handlers
import constants


def get_logger():
    handler = logging.StreamHandler()
    # fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    fmt = ''
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = logging.getLogger(constants.PACKAGE_NAME)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


LOG = get_logger()
