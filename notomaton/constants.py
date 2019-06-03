from enum import Enum

class Product(Enum):
    ZENKO = 1
    S3C = 2
    RING = 3

PRODUCT_TO_NAME = {
    Product.ZENKO: 'Zenko',
    Product.S3C: 'S3 Connector',
    Product.RING: 'Ring',
}

PRODUCT_TO_CANONICAL = {
    Product.ZENKO: 'zenko',
    Product.S3C: 's3c',
    Product.RING: 'ring'
}

CANONICAL_TO_PRODUCT = {
    'zenko': Product.ZENKO,
    's3c': Product.S3C,
    'ring': Product.RING
}
