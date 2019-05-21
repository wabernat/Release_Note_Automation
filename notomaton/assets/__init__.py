from pathlib import PosixPath
from collections import defaultdict

from ..util.log import Log

_log = Log('assets')

_ASSETS = defaultdict(dict)

def _load_assets():
    for dir_path in PosixPath(__file__).parent.resolve().iterdir():
        if dir_path.is_file():
            continue
        for file_path in dir_path.iterdir():
            if file_path.is_file() and not 'py' in file_path.suffix:
                if file_path.name in _ASSETS[dir_path.name]:
                    raise Exception(
                        'Asset with name %s.%s is already registered! (%s)',
                        dir_path.name,
                        path.name,
                        file_path.as_posix()
                    )
                _log.debug('Loading asset %s.%s (%s)',
                    dir_path.name,
                    file_path.stem,
                    file_path.as_posix()
                )
                try:
                    with open(file_path) as asset:
                        _ASSETS[dir_path.name][file_path.stem] = asset.read()
                except Exception as e:
                    print('err')
                    raise e
                _log.debug(
                    'Loaded asset %s.%s (%s)',
                    dir_path.name,
                    file_path.stem,
                    file_path.as_posix()
                )
_load_assets()


def get_asset(name):
    return _ASSETS.get(name)
