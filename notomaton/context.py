from collections import namedtuple

from .constants import PRODUCT_TO_NAME, PRODUCT_TO_CANONICAL, PRODUCT_DOC_NAME
from .search import do_search
from .assets import discover_images

Context = namedtuple('Context', ['product', 'issues', 'style', 'images', 'is_dashboard'])

Issues = namedtuple('Issues', ['known', 'fixed', 'new_features', 'improvements'])

Product = namedtuple('Product', ['name', 'canonical', 'version', 'doc_name'])

def build_issues(product, version):
    search = do_search(product, version)
    return Issues(
        known = tuple(search.known),
        fixed = tuple(search.fixed),
        new_features=tuple(search.new_features),
        improvements=tuple(search.improvements)
    )

def build_images():
    images = discover_images()
    nt = namedtuple('Images', list(images.keys()))
    return nt(**{ k: v.encode() for k, v in images.items()})

def build_context(product, version, dashboard=False):
    return Context(
        style=None, # Will be injected later
        product = Product(
            name=PRODUCT_TO_NAME[product],
            canonical=PRODUCT_TO_CANONICAL[product],
            version=version,
            doc_name=PRODUCT_DOC_NAME[product]
        ),
        issues = build_issues(product, version),
        images = build_images(),
        is_dashboard=dashboard,
    )
