from collections import namedtuple

from jira import JIRA

from .util.conf import config
from .util.log import Log

_log = Log('jira')

Ticket = namedtuple('Ticket', ['key', 'severity', 'components', 'description', 'fix_versions'])

def _get_jira():
    return JIRA(server = config.jira.server, basic_auth=(config.jira.user, config.jira.token))

def get_issues(query):
    _log.info('Using jql %s'%query)
    for ticket in _get_jira().search_issues(query):
        yield Ticket(
            ticket.key, # Ticket ID eg ZENKO-1234
            getattr(ticket.fields.customfield_10800, 'value', '--'), # Severity
            [c.name for c in ticket.fields.components], # Component names
            ticket.fields.description, # Ticket description
            [v.name for v in ticket.fields.fixVersions] # Fix version
        )
