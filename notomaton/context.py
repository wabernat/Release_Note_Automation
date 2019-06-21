from collections import namedtuple

from .constants import PRODUCT_TO_NAME, PRODUCT_TO_CANONICAL
from .search import do_search

Context = namedtuple('Context', ['product', 'issues', 'style'])

Issues = namedtuple('Issues', ['known', 'fixed'])

Product = namedtuple('Product', ['name', 'canonical', 'version'])

def build_issues(product, version):
    search = do_search(product, version)
    return Issues(
        known = tuple(search.known),
        fixed = tuple(search.fixed)
    )

def build_context(product, version):
    return Context(
        style=None, # Will be injected later
        product = Product(
            name=PRODUCT_TO_NAME[product],
            canonical=PRODUCT_TO_CANONICAL[product],
            version=version
        ),
        issues = build_issues(product, version)
    )
