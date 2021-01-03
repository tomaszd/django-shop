
from shop.search.documents import ProductDocument

settings = {
    'number_of_shards': 1,
    'number_of_replicas': 0,
}
ProductDocument(settings=settings)
