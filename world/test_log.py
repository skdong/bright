import logging
import logging.handlers

handler = logging.StreamHandler()
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('a')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info('first info message')
logger.debug('first debug message')
