from jira import JIRA

from .util.conf import config
from .util.log import Log

_log = Log('jira')


def get_jira():
    return JIRA(server = config.jira.server, basic_auth=(config.jira.user, config.jira.token))
