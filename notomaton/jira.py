from collections import namedtuple

from jira import JIRA

from .util.conf import config
from .util.log import Log

_log = Log('jira')

BASE_JQL = 'project = {project} AND fixVersion >= {version} AND "Release notes" != "No" AND status {fixed} "Done"'

Ticket = namedtuple('Ticket', ['key', 'severity', 'components', 'description'])



    # known issues:
    #     Query: Project AND fixVersion number AND (Release Notes != "No" or "None") AND status != "Done"
    #     jq-filter results to produce a table with Key, Severity, Components, and Release Notes Description.
    #     Name this table "[known]-[product]-[version].html"
    # fixed issues:
    #     Query: Project AND fixVersion number AND (Release Notes != "No" or "None") AND status = "Done"
    #     jq-filter results to produce a table with Key, Severity, Components, and Release Notes Description.
    #     Name this table "[fixed]-[product]-[version].html"




def _get_jira():
    return JIRA(server = config.jira.server, basic_auth=(config.jira.user, config.jira.token))


def _build_jql(project, version, fixed=False):
    fixed = '=' if fixed else '!='
    return BASE_JQL.format(project=project, version=version, fixed=fixed)


def _get_issues(query):
    for ticket in _get_jira().search_issues(query):
        yield Ticket(
            ticket.key, # Ticket ID eg ZENKO-1234
            ticket.fields.customfield_10800.value, # Severity
            [c.name for c in ticket.fields.components], # Component names
            ticket.fields.customfield_12102, # Ticket description
        )


def get_issues(project, version, fixed):
    query = _build_jql(project, version, fixed)
    _log.info('Using jql %s'%query)
    return list(_get_issues(query))

def get_known(project, version):
    return get_issues(project, version, False)

def get_fixed(project, version):
    return get_issues(project, version, True)
