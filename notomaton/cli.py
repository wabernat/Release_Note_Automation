import argparse

from .util.arg import flag, option


@flag('--verbose', dest='logging.loglvl')
def verbose(*args, **kwargs):
	return 'debug'

@option('-p', '--project', dest='runtime.project', metavar='PROJECT',
		required=True, help='Jira project')
def project(value):
    return value

@option('-v', '--version', dest='runtime.version', metavar='VERSION',
		required=True, help='Project version >=')
def version(value):
    return value

@option('-u', '--user', dest='jira.user', metavar='USER',
		help='Jira user')
def user(value):
    return value

@option('-t', '--token', dest='jira.token', metavar='TOKEN',
		help='Jira token')
def token(value):
    return value

@option('-s', '--server', dest='jira.server', metavar='SERVER',
		help='Jira server')
def server(value):
    return value

@option('-f', '--file', dest='runtime.output', metavar='FILE', type=argparse.FileType('w'), help='File path to write html output')
def file(value):
	return value
