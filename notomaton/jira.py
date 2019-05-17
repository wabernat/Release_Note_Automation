from collections import namedtuple
from pprint import pprint
from itertools import chain
from jira import JIRA

from .util.conf import config
from .util.log import Log
import json

_log = Log('jira')

Ticket = namedtuple('Ticket', ['key', 'severity', 'components', 'description', 'fix_versions'])

JQL_MATRIX = [
    'project = {project}',
    '"Release notes" != "No"',
    'status {fixed} "Done"',
    'issuetype = bug',
    '(severity in (Critical, Blocker) OR priority in (High, Urgent) AND severity = Major)',
    'fixVersion >= {version}'
]

ISSUE_ORDERING = 'ORDER BY status, severity, priority'

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
    if project == 'zenko':
        # Zenko has alpanumeric version so leave off the fixVersion
        tmpl = ' AND '.join(JQL_MATRIX[:-1])
    else:
        tmpl = ' AND '.join(JQL_MATRIX)
    tmpl += ' ' + ISSUE_ORDERING
    fixed = '=' if fixed else '!='
    return tmpl.format(project=project, version=version, fixed=fixed)

def _parse_version(ver):
    try:
        major, minor, patch = ver.split('.')
        return int(major), int(minor), int(patch)
    except ValueError:
        return None

def _get_issues(query):
    _log.info('Using jql %s'%query)
    for ticket in _get_jira().search_issues(query):
        yield Ticket(
            ticket.key, # Ticket ID eg ZENKO-1234
            getattr(ticket.fields.customfield_10800, 'value', '--'), # Severity
            [c.name for c in ticket.fields.components], # Component names
            ticket.fields.customfield_12102, # Ticket description
            [v.name for v in ticket.fields.fixVersions] # Fix version
        )

def _get_issues_zenko(version, fixed):
    query = _build_jql('zenko', version, fixed)
    to_meet = _parse_version(version)
    for ticket in _get_issues(query):  # Zenko has alphanumeric versions
        for v in ticket.fix_versions:  # in addition to semantic, so we manually check
            ticket_version = _parse_version(v)
            if ticket_version is not None and ticket_version >= to_meet:
                yield ticket
                break

def _get_issues_s3c(version, fixed):
    for p in ['s3c', 'md']: # S3C release notes contain Metadata tickets too
        query = _build_jql(p, version, fixed)
        for t in _get_issues(query):
            yield t

def _get_issues_generic(project, version, fixed):
    query = _build_jql(project, version , fixed)
    return _get_issues(query)

def get_issues(project, version, fixed):
    if project == 'zenko':
        issues = _get_issues_zenko(version, fixed)
    elif project == 's3c':
        issues = _get_issues_s3c(version, fixed)
    else:
        issues = _get_issues_generic(project, version, fixed)
    return list(
        sorted(issues, key=lambda i: i.severity)
    )

def get_known(project, version):
    return get_issues(project, version, False)

def get_fixed(project, version):
    return get_issues(project, version, True)
