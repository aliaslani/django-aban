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
