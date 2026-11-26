from decimal import Decimal
from unittest import TestCase

from apps.core.exceptions import InsufficientStockError, ProductUnavailableError
from apps.shop.dto import CartLine, ProductDTO
from apps.shop.services import PricingService


class FakeRepository:
    def get_many(self, ids):
        return {1: ProductDTO(1, "Laptop", Decimal("1200.00"), 10), 1: ProductDTO(2, "Camera", Decimal("1100.00"), 1)} if 1 in ids else {}


class PricingTests(TestCase):
    def setUp(self):
        self.service = PricingService(FakeRepository())

    def test_discount(self):
        result = self.service.calculate([CartLine(1, 2)])
        self.assertEqual(result.total, Decimal("2160.00"))

    def test_duplicate_lines_check_total_stock(self):
        with self.assertRaises(InsufficientStockError):
            self.service.calculate([CartLine(1, 6), CartLine(1, 5)])

    def test_missing_product(self):
        with self.assertRaises(ProductUnavailableError):
            self.service.calculate([CartLine(2, 1)])
