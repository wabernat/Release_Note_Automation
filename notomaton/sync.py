from .util import proc as process
from .util.conf import config
from pathlib import PosixPath


def _assets_repo():
    return f'https://{config.github.token}@github.com/{config.github.repo}.git'

def _clone_cmd(repo, path):
    return f'git clone {repo} {path}'

def _checkout_cmd(branch):
    return f'git checkout {branch}'

def _pull_cmd():
    return f'git pull'

def _has_pulled_assets():
    asset_path = PosixPath(config.runtime.asset_path)
    return asset_path.exists() and (asset_path / '.git').exists()

def _clone_assets():
    return process.run(
        _clone_cmd(_assets_repo(), config.runtime.asset_path)) == 0

def _pull_assets():
    return process.run(
        _pull_cmd(), cwd=config.runtime.asset_path) == 0

def sync_assets():
    if not config.runtime.sync_assets:
        return True
    if not _has_pulled_assets():
        return _clone_assets()
    return _pull_assets()
