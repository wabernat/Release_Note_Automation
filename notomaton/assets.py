from collections import namedtuple
from itertools import chain
from pathlib import PosixPath

import yaml
from jinja2 import Template as JinjaTemplate

from .util.conf import config

_ASSETS = []

VALID_EXTENSIONS = [
    '.html',
    '.css',
]

BASE_HTML = '<?xml version="1.0" encoding="utf-8"?><html>{book}</html>'

class Template:
    def __init__(self, path, **kwargs):
        self._tmpl_path = path
        self._tmpl_args = kwargs

    def _load_tmpl(self):
        with open(self._tmpl_path) as tmpl:
            return JinjaTemplate(tmpl.read())

    def _get_from_context(self, ctx, path):
        parts = path.replace('$ctx.', '').split('.')
        val = ctx
        for key in parts:
            val = getattr(val, key)
            if val is None:
                raise Exception('Unable to locate key %s', key)
        return val

    def _resolve_args(self, ctx):
        args = {}
        for key, value in self._tmpl_args.items():
            if value.startswith('$ctx'):
                value = self._get_from_context(ctx, value)
            args[key] = value
        return args

    def _inject_args(self, ctx):
        _ctx = ctx._asdict()
        new_ctx = namedtuple('Context', list(chain(_ctx.keys(), self._tmpl_args.keys())))
        args = self._resolve_args(ctx)
        _ctx.update(args)
        return new_ctx(**_ctx)

    @property
    def text(self):
        with open(self._tmpl_path) as tmpl:
            return tmpl.read()

    def render(self, ctx):
        return self._load_tmpl().render(
            ctx=self._inject_args(ctx)
        )

class Assets:
    def __init__(self, assets):
        self._assets = assets

    def __repr__(self):
        return str(self._assets)

    def exists(self, path):
        return path in self._assets

    def get(self, path):
        if self.exists(path):
            return self._assets.get(path)
        raise Exception('Unable to locate asset %s'%path)

    def render(path):
        if self.exists(path):
            tmpl = Template(self.get(path))

class Book:
    def __init__(self, name, version):
        self._name = name
        self._version = version

    @property
    def _version_str(self):
        return '.'.join(str(i) for i in self._version)

    def _load_style(self):
        book = load_book(self._name, self._version)
        return book['style']

    def _load_pages(self):
        book = load_book(self._name, self._version)
        return book['layout']

    def _load_assets(self):
        return discover_assets()

    def _resolve_files(self, files, assets):
        resolved_files = []
        for path in files:
            if not '/' in path:
                path = f'{self._name}/{self._version}/{path}'
            resolved_files.append(assets.get(path))
        return resolved_files

    def _resolve_style(self, style, assets):
        return '\n'.join([f.text for f in self._resolve_files(
                style, assets
            )]
        )

    def _resolve_layout(self, pages, assets):
        return self._resolve_files(pages, assets)


    def _get_layout(self, assets):
        return self._resolve_layout(
            self._load_pages(),
            self._load_assets()
        )

    def _inject_style(self, style, ctx):
        return ctx._replace(style=style)

    def render(self, ctx):
        assets = self._load_assets()
        style = self._resolve_style(self._load_style(), assets)
        ctx = self._inject_style(style, ctx)
        return BASE_HTML.format(
            book='\n'.join(page.render(ctx) for page in self._get_layout(assets))
        )


def find_files(directory):
    for path in directory.iterdir():
        if path.is_dir():
            for subpath in find_files(path):
                yield subpath
        else:
            yield path

def discover_templates():
    template_paths = {}
    template_dir = PosixPath(config.runtime.asset_path).resolve() / 'templates'
    for path in find_files(template_dir):
        if path.is_file() and path.suffix == '.j2':
            template_paths[path.stem] = path
    with open(template_dir / 'templates.yaml') as template_conffile:
        template_conf = yaml.safe_load(template_conffile)
    templates = {}
    for template_base, conf in template_conf['templates'].items():
        if not template_base in template_paths:
            raise Exception('Unknown template %s'%template_base)
        for variant, args in conf.items():
            template_name = '$templates/%s.%s'%(template_base, variant)
            templates[template_name] = Template(template_paths[template_base], **args)
    return templates

def discover_assets():
    assets = {}
    asset_dir = PosixPath(config.runtime.asset_path).resolve() / 'assets'
    for path in find_files(asset_dir):
        if path.is_file() and path.suffix in VALID_EXTENSIONS:
            asset_path = path.relative_to(asset_dir).as_posix()
            assets[asset_path] = Template(path)
    assets.update(discover_templates())
    return Assets(assets)

def get_asset(path):
    asset_path = PosixPath(config.runtime.asset_path).resolve() / 'assets' / path
    if not asset_path.exists() or not asset_path.is_file():
        raise Exception('Unable to load asset %s at %s', (path, asset_path))
    with open(asset_path) as f:
        return f.read()

def load_book(name, version):
    asset_dir = PosixPath(config.runtime.asset_path).resolve() / 'assets'
    # version_string = '.'.join(str(i) for i in version)
    book_dir = asset_dir / name / version
    if not book_dir.exists():
        raise Exception(f'Unable to locate book {name}/{version}')
    elif not book_dir.is_dir():
        raise Exception(f'Expected book directory is a file! assets/{name}/{version}')
    elif not book_dir.joinpath('layout.yaml').exists():
        raise Exception(f'Unable to locate book layout.yaml for {name}/{version}')
    with open(book_dir.joinpath('layout.yaml')) as book:
        book_layout = yaml.safe_load(book)
        return book_layout


def resolve_book(book, assets):
    pages = []
    for page in book['layout']:
        pages.append(assets.get(page))
    return pages
