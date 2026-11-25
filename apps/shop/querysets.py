from django.db import models


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def in_stock(self):
        return self.filter(stock__gt=0)

    def out_of_stock(self):
        return self.filter(stock=0)

    def available(self):
        return self.active().in_stock()


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    pass
