from .util.arg import flag, option

@flag('--verbose', dest='logging.loglvl')
def verbose(*args, **kwargs):
	return 'debug'

@option('-p', '--project', dest='runtime.project')
def project(value):
    return value

@option('-v', '--version', dest='runtime.version')
def version(value):
    return value

@option('-u', '--user', dest='jira.user')
def user(value):
    return value

@option('-t', '--token', dest='jira.token')
def token(value):
    return value

@option('-s', '--server', dest='jira.server')
def server(value):
    return value
