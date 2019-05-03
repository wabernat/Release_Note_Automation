from collections import namedtuple

from jira import JIRA

from .util.conf import config
from .util.log import Log

_log = Log('jira')

BASE_JQL = 'project = {project} AND fixVersion >= {version} AND status = done AND "Release notes" = "Yes as Fixed Issue only (please fill Release Note)"'

Ticket = namedtuple('Ticket', ['key', 'severity', 'components', 'description'])


def _get_jira():
    return JIRA(server = config.jira.server, basic_auth=(config.jira.user, config.jira.token))


def _build_jql(project, version):
    return BASE_JQL.format(project=project, version=version)


def _get_issues(query):
    for ticket in _get_jira().search_issues(query):
        yield Ticket(
            ticket.key, # Ticket ID eg ZENKO-1234
            ticket.fields.customfield_10800.value, # Severity
            [c.name for c in ticket.fields.components], # Component names
            ticket.fields.customfield_12102, # Ticket description
        )


def get_issues(project, version):
    query = _build_jql(project, version)
    _log.debug('Using jql %s'%query)
    return list(_get_issues(query))
