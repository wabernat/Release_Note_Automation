from .util.arg import flag, option

@flag('--verbose', dest='logging.loglvl')
def verbose(*args, **kwargs):
	return 'debug'

@option('-p', '--project', dest='runtime.project', metavar='PROJECT')
def project(value):
    return value

@option('-v', '--version', dest='runtime.version', metavar='VERSION')
def version(value):
    return value

@option('-u', '--user', dest='jira.user', metavar='USER')
def user(value):
    return value

@option('-t', '--token', dest='jira.token', metavar='TOKEN')
def token(value):
    return value

@option('-s', '--server', dest='jira.server', metavar='SERVER')
def server(value):
    return value
