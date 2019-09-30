import re
from collections import namedtuple
from .constants import TicketType

Ticket = namedtuple('Ticket', ['key', 'severity', 'components', 'description', 'fix_versions', 'type', 'title', 'in_release_notes'])

CODE_BLOCK_REGEX = r'{code(?::\w+)?}'
NO_FORMAT_REGEX = r'{noformat}'

REPL_START = '<pre><code>'
REPL_STOP = '</code></pre>'

def _replace_tag(tag, repl, string):
    new_string, replaced = re.subn(tag, repl, string, count=1)
    return replaced == 1, new_string

def _replace_block(regex, string):
    changed = True
    new_string = string
    while changed:
        changed, new_string = _replace_tag(regex, REPL_START, new_string)
        if changed: # If we replace a starting tag we require a end tag
            changed, new_string = _replace_tag(regex, REPL_STOP, new_string)
            if not changed:
                _log.error('Unable to end tag for block!')
                _log.debug(string)
    return new_string

def replace_no_format(string):
    return _replace_block(NO_FORMAT_REGEX, string)

def replace_code_block(string):
    return _replace_block(CODE_BLOCK_REGEX, string)

def replace_jira_formatting(string):
    if string is None:
        return ''
    return replace_code_block(replace_no_format(string))

def safe_extract(ticket):
    ticket_type = TicketType(int(ticket.fields.issuetype.id))
    fields = dict(key=ticket.key, type=ticket_type)
    # Extract description
    if hasattr(ticket.fields, 'customfield_12102') and \
        ticket.fields.customfield_12102 and \
        ticket.fields.customfield_12102.strip():
        fields['description'] = replace_jira_formatting(ticket.fields.customfield_12102)
    elif ticket_type == TicketType.EPIC and hasattr(ticket.fields, 'description'):
        fields['description'] = ticket.fields.description
    else:
        fields['description'] = ''
    # Extract Release Notes field
    if hasattr(ticket.fields, 'customfield_12101') and ticket.fields.customfield_12101:
        fields['in_release_notes'] = ticket.fields.customfield_12101.value != 'No'
    else:
        fields['in_release_notes'] = True
    # Extract severity
    if hasattr(ticket.fields,'customfield_10800'):
        fields['severity'] = getattr(ticket.fields.customfield_10800,
                                        'value', '--')
    else:
        fields['severity'] = '--'
    # Extract components
    if hasattr(ticket.fields, 'components'):
        fields['components'] = [c.name for c in ticket.fields.components]
    else:
        fields['components'] = []
    # Extract fix_versions
    if hasattr(ticket.fields, 'fixVersions'):
        fields['fix_versions'] = [v.name for v in ticket.fields.fixVersions]
    else:
        fields['fix_versions'] = []
    # Extract title
    if hasattr(ticket.fields, 'summary'):
        fields['title'] = ticket.fields.summary
    else:
        fields['title'] = ''
    return fields

def build_ticket(ticket):
    return Ticket(**safe_extract(ticket))
