from oslo_config import cfg
from oslo_log import log as logging
from oslo_context import context

CONF = cfg.CONF
DOMAIN = "demo"

logging.register_options(CONF)
logging.setup(CONF, DOMAIN)

LOG = logging.getLogger(DOMAIN)

LOG.info("Message without context")
con = context.RequestContext()
LOG.info("Message with  context")
cont_new = context.RequestContext(user='test',
                       tenant='test_project',
                       project_domain='test_domain')
LOG.info("Message with new context")
LOG.info("Message with con", context=con)
LOG.info("Message with new")