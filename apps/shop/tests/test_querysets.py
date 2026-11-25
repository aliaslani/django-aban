from django.test import TestCase

from apps.core.exceptions import InsufficientStockError
from apps.shop.models import Product
from apps.shop.services import InventoryService


class ProductTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Laptop", price="1200.00", stock=2)
        Product.objects.create(name="Inactive", price="20.00", stock=2, is_active=False)

    def test_available(self):
        self.assertEqual(list(Product.objects.available()), [self.product])

    def test_inventory(self):
        InventoryService.decrease_stock(self.product.pk, 2)
        with self.assertRaises(InsufficientStockError):
            InventoryService.decrease_stock(self.product.pk, 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 0)
