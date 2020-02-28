from enum import Enum

class Product(Enum):
    ZENKO = 1
    RING = 3

PRODUCT_TO_NAME = {
    Product.ZENKO: 'Zenko',
    Product.RING: 'RING',
}

PRODUCT_TO_CANONICAL = {
    Product.ZENKO: 'zenko',
    Product.RING: 'ring'
}

CANONICAL_TO_PRODUCT = {
    'zenko': Product.ZENKO,
    'ring': Product.RING
}

PRODUCT_DOC_NAME = {
    Product.ZENKO: 'Zenko',
    Product.RING: 'RING',
}

class TicketType(Enum):
    BUG = 1
    IMPROVEMENT = 4
    EPIC = 10000
