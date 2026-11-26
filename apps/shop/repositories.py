from .dto import ProductDTO
from .models import Product


class DjangoProductRepository:
    def get_many(self, ids):
        rows = (
            Product.objects.active()
            .filter(pk__in=ids)
            .values("id", "name", "price", "stock")
        )
        return {row["id"]: ProductDTO(**row) for row in rows}

    def list_active(self):
        return Product.objects.active()


class InMemoryProductRepository:
    def __init__(self,products):
        self.products = {
            product.id: product for product in products
        }

    def get_many(self, ids):
        return {
            product_id: self.products[product_id] for product_id in ids
            if product_id in self.products
        }