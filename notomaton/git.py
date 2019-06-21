from github import Github, GithubException
from .util.conf import config
import requests

def _get_github():
    return Github(config.github.token)

def _get_asset_repo():
    return _get_github().get_repo(config.github.repo)

def get_latest_revision():
    try:
        branch = _get_asset_repo().get_branch(config.github.branch)
        return branch.commit.sha
    except GithubException:
        pass


def download_revision(sha):
    return _get_asset_repo().get_archive_link('tarball', sha)
