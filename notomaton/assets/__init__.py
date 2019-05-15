from pathlib import PosixPath

from ..util.log import Log

_log = Log('assets')

_ASSETS = {}

def _load_assets():
    for path in PosixPath(__file__).parent.resolve().iterdir():
        if path.is_file() and path.suffix != '.py' and not path.name in _ASSETS:
            with open(path) as asset:
                _ASSETS[path.stem] = asset.read()
            _log.debug('Loaded asset %s (%s)'%(path.stem, path))


_load_assets()


def get_asset(name):
    return _ASSETS.get(name)
