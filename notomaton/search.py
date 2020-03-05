from .constants import Product, TicketType
from .jira import get_jira
from .util.log import Log
from .util.ticket import parse_version, ring_to_s3c_version
from .ticket import build_ticket

import itertools

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

    def _release_notes_filter(self):
        return '"Release notes" != "No"'

    def _release_notes_epic_filter(self):
        return '("Release notes" is EMPTY OR "Release notes" != No)'

    def _gte_version_filter(self):
        return f'fixVersion >= {self._version}'

    def _equ_version_filter(self):
        return f'fixVersion = {self._version}'

    def _issue_type_filter_bug(self):
        return 'issuetype = bug'

    def _issue_type_filter_epic(self):
        return 'issuetype = epic'

    def _issue_type_filter_improvement(self):
        return 'issuetype = improvement'

    def _ticket_filter(self):
        return '(severity in (Critical, Blocker) OR ' + \
            '(priority in (High, Urgent) AND severity = Major))'

    def _fixed_filter(self):
        return 'status = "Done" AND resolution in (fixed, done)'

    def _known_filter(self):
        return '''(status != "Done" OR (status = "Done" AND resolution = "Won't Fix"))'''

    def _feature_filter(self, tickets):
        for ticket in tickets:
            if ticket.type == TicketType.EPIC or ticket.in_release_notes:
                yield ticket

    def _build_jql(self, *args):
        filter_funcs = [
            self._project_filter,
            *args
        ]
        filters = []
        for filter_func  in filter_funcs:
            ticket_filter = filter_func()
            if ticket_filter:
                filters.append(ticket_filter)
        _log.debug(filters)
        return '%s %s'%(' AND '.join(filters), self._ordering)

    def _get_issues(self, *args):
        query = self._build_jql(*args)
        _log.info('Using jql %s'%query)
        try:
            for ticket in get_jira().search_issues(query, maxResults=False):
                # print(vars(ticket))
                yield build_ticket(ticket)
        except Exception:
            pass

    def _sort_issues(self, issues, key='severity', **kwargs):
        return tuple(
            sorted(
                list(issues),
                key=lambda i: getattr(i, key),
                **kwargs
            )
        )

    @property
    def fixed(self):
        return self._sort_issues(
            self._get_issues(
                self._release_notes_filter,
                self._fixed_filter,
                self._equ_version_filter,
                self._issue_type_filter_bug,
                self._ticket_filter,
            )
        )

    @property
    def known(self):
        return self._sort_issues(
            self._get_issues(
                self._release_notes_filter,
                self._known_filter,
                self._gte_version_filter,
                self._issue_type_filter_bug,
                self._ticket_filter,
            )
        )

    @property
    def new_features(self):
        return list(self._feature_filter(
            self._sort_issues(
                self._get_issues(
                    self._release_notes_epic_filter,
                    self._fixed_filter,
                    self._equ_version_filter,
                    self._issue_type_filter_epic
                )
            )
        ))

    @property
    def improvements(self):
        return list(self._feature_filter(
            self._sort_issues(
                self._get_issues(
                    self._fixed_filter,
                    self._equ_version_filter,
                    self._issue_type_filter_improvement
                )
            )
        ))

class ZenkoSearch(JiraSearch):
    # We filter Zenko version manually as they are alphanumeric
    def __init__(self, version):
        super().__init__(('zenko', 'zenkoio', 'ob'), version)

    def _gte_version_filter(self):
        return ''

    def _equ_version_filter(self):
        return ''

    def __filter_tickets(self, tickets, cmp):
        to_meet = parse_version(self._version)
        for ticket in tickets:
            for version in ticket.fix_versions:
                ticket_version = parse_version(version)
                if ticket_version is not None and cmp(ticket_version, to_meet):
                    yield ticket
                    break

    def __equ_version_filter(self, tickets):
        return self.__filter_tickets(tickets, lambda x, y: x == y)

    def __gte_version_filter(self, tickets):
        return self.__filter_tickets(tickets, lambda x, y: x >= y)

    @property
    def fixed(self):
        return list(self.__equ_version_filter(super().fixed))

    @property
    def known(self):
        return list(self.__gte_version_filter(super().known))

    @property
    def new_features(self):
        return list(self.__equ_version_filter(super().new_features))

class S3CSearch(JiraSearch):
    def __init__(self, version):
        super().__init__(('s3c', 'md'), version)

class RingSearch(JiraSearch):
    def __init__(self, version):
        super().__init__('ring', version)
        self._s3c_search = S3CSearch(ring_to_s3c_version(version))

    @property
    def fixed(self):
        return self._sort_issues(
            itertools.chain(super().fixed, self._s3c_search.fixed)
        )

    @property
    def known(self):
        return self._sort_issues(
            itertools.chain(super().known, self._s3c_search.known)
        )

    @property
    def new_features(self):
        return self._sort_issues(
            itertools.chain(super().new_features, self._s3c_search.new_features)
        )

    @property
    def improvements(self):
        return self._sort_issues(
            itertools.chain(super().improvements, self._s3c_search.improvements)
        )


PRODUCT_TO_SEARCH = {
    Product.ZENKO: ZenkoSearch,
    Product.S3C: S3CSearch,
    Product.RING: RingSearch
}

def do_search(product, version):
    return PRODUCT_TO_SEARCH[product](version[:5])
