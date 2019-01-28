from pathlib import PosixPath

from jinja2 import Template

from ..util.log import Log

_log = Log('templates')

_TEMPLATES = {}

def _load_templates():
    for path in PosixPath(__file__).parent.resolve().iterdir():
        if path.is_file() and path.suffix == '.j2' and not path.name in _TEMPLATES:
            _TEMPLATES[path.stem] = Template(open(path).read())
            _log.debug('Loaded template %s (%s)'%(path.stem, path))


_load_templates()


def get_template(name):
    return _TEMPLATES.get(name)
