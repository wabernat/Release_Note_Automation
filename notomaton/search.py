from .constants import Product
from .jira import Ticket, get_jira
from .util.log import Log
from .util.ticket import parse_version

_log = Log('search')

class JiraSearch:
    _ordering = 'ORDER BY status, severity, priority'
    def __init__(self, project, version):
        self._project = project
        self._version = version

    def _project_filter(self):
        if isinstance(self._project, tuple) or isinstance(self._project, list):
            jql = ' OR '.join(f'project = {p}' for p in self._project)
            return f'({jql})'
        return f'project = {self._project}'

    def _version_filter(self):
        return f'fixVersion >= {self._version}'

        return 'status != "Done"'

    def _ticket_filter(self):
        return '(severity in (Critical, Blocker) OR ' + \
            'priority in (High, Urgent) AND severity = Major)'

    def _fixed_filter(self):
        return 'status = "Done" AND resolution in (fixed, done)'

    def _known_filter(self):
        return 'status != "Done"'

    def _build_jql(self, *args):
        filter_funcs = [
            self._project_filter,
            self._version_filter,
            self._ticket_filter,
            *args
        ]
        filters = []
        for filter_func  in filter_funcs:
            ticket_filter = filter_func()
            if ticket_filter:
                filters.append(ticket_filter)
        return '%s %s'%(' AND '.join(filters), self._ordering)

    def _get_fields(self, ticket):
        fields = dict(
            key=ticket.key,
            description=ticket.fields.description
        )
        fields['severity'] = getattr(ticket.fields.customfield_10800,
                                        'value', '--')
        fields['components'] = [c.name for c in ticket.fields.components]
        fields['fix_versions'] = [v.name for v in ticket.fields.fixVersions]
        return fields

    def _get_issues(self, *args):
        query = self._build_jql(*args)
        _log.info('Using jql %s'%query)
        for ticket in get_jira().search_issues(query):
            yield Ticket(**self._get_fields(ticket))

    def _sort_issues(self, issues):
        return tuple(
            sorted(
                list(issues),
                key=lambda i: i.severity
            )
        )

    @property
    def fixed(self):
        return self._sort_issues(
            self._get_issues(
                self._fixed_filter
            )
        )

    @property
    def known(self):
        return self._sort_issues(
            self._get_issues(
               self._known_filter
            )
        )

class ZenkoSearch(JiraSearch):
    # We filter Zenko version manually as they are alphanumeric
    def __init__(self, version):
        super().__init__(('zenko', 'znc'), version)

    def _version_filter(self):
        return ''

    def _get_issues(self, *args):
        to_meet = parse_version(self._version)
        for ticket in super()._get_issues(*args):
            for version in ticket.fix_versions:
                ticket_version = parse_version(version)
                if ticket_version is not None and ticket_version >= to_meet:
                    yield ticket
                    break

class S3CSearch(JiraSearch):
    def __init__(self, version):
        super().__init__(('s3c', 'md'), version)

class RingSearch(JiraSearch):
    def __init__(self, version):
        super().__init__('ring', version)

    def _get_fields(self, ticket):
        fields = super()._get_fields(ticket)
        if hasattr(ticket.fields, 'customfield_12102') and \
            ticket.fields.customfield_12102 and \
            ticket.fields.customfield_12102.strip():
            fields['description'] = ticket.fields.customfield_12102
        return fields

PRODUCT_TO_SEARCH = {
    Product.ZENKO: ZenkoSearch,
    Product.S3C: S3CSearch,
    Product.RING: RingSearch
}

def do_search(product, version):
    return PRODUCT_TO_SEARCH[product](version)
