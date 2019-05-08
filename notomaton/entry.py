import logging
import sys

from .jira import get_known, get_fixed
from .render import render_template
from .util.conf import config
from .util.log import Log
from .util.prompt import prompt

_log = Log('entry')

def entry():
    try:
        main()
    except Exception as e:
        # if config.logging.loglvl == logging.DEBUG:
        # else:
        _log.exception(e)
        _log.critical('Error!')
        sys.exit(1)

FILENAME_TMPL = '{type}-{project}-{version}.html'

def main():
    conf = prompt(['project', 'version'])
    known_issues = get_known(conf['project'].upper(), conf['version'])
    fixed_issues = get_fixed(conf['project'].upper(), conf['version'])
    conf['type'] = 'known'
    with open(FILENAME_TMPL.format(**conf), 'w') as f:
        f.write(
            render_template(config.runtime.template, notes=known_issues)
        )
    conf['type'] = 'fixed'
    with open(FILENAME_TMPL.format(**conf), 'w') as f:
        f.write(
            render_template(config.runtime.template, notes=fixed_issues)
        )
