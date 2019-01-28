import logging
import sys

from .jira import get_issues
from .render import render_template
from .util.conf import config
from .util.log import Log

_log = Log('entry')

def entry():
    try:
        main()
    except Exception as e:
        if config.logging.loglvl == logging.DEBUG:
            raise(e)
        else:
            print('Error!')
        sys.exit(1)


def main():
    issues = get_issues(config.runtime.project, config.runtime.version)
    print(render_template(config.runtime.template, notes=issues))
