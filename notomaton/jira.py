from collections import namedtuple
import re

from jira import JIRA

from .util.conf import config
from .util.log import Log

_log = Log('jira')

Ticket = namedtuple('Ticket', ['key', 'severity', 'components', 'description', 'fix_versions'])

def get_jira():
    return JIRA(server = config.jira.server, basic_auth=(config.jira.user, config.jira.token))


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
