import re
from collections import namedtuple
from .constants import TicketType
from functools import partial
from .util.log import Log

_log = Log('ticket')

Ticket = namedtuple('Ticket', ['key', 'severity', 'components', 'description', 'fix_versions', 'type', 'title', 'in_release_notes'])

# Old JIRA format
CODE_BLOCK_REGEX = r'{code(?::\w+)?}(.*?){code}' 
NO_FORMAT_REGEX = r'{noformat}(.*?){noformat}'



REPL_START = '<pre><code>'
REPL_STOP = '</code></pre>'

REPL_BLOCKS = {
    'code_block_old': {
        'regex': r'{code(?::\w+)?}(.*?){code}',
        'replace': '<pre><code>{text}</code></pre>'
    },
    'no_format_old': {
        'regex': r'{noformat}(.*?){noformat}',
        'replace': '<pre><code>{text}</code></pre>'
    },
    'code_block': {
        'regex': r' {{(.*?)}} ',
        'replace': '<pre><code> {text} </code></pre>'
    },
    'italic_text': {
        'regex': r' _(.*?)_ ',
        'replace': '<i> {text} </i>'
    },
    'bold_text': {
        'regex': r' \*(.*?)\* ',
        'replace': '<b> {text} </b>'
    },
    'strikethru_text': {
        'regex': r' -(.*?)- ',
        'replace': '<strike> {text} </strike>'
    }
}

def _format_block(tmpl, match):
    return tmpl.format(text=match.group(1))

def _replace_block(block_type, text):
    block = REPL_BLOCKS[block_type]
    _repl_func = partial(_format_block, block['replace'])
    replaced, count = re.subn(block['regex'], _repl_func, text, flags=re.S)
    _log.debug('Replaced {count} occurrences of {block_type}')
    return replaced

def replace_jira_formatting(string):
    if string is None:
        return ''
    for block_type in REPL_BLOCKS.keys():
        string = _replace_block(block_type, string)
    return string

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
