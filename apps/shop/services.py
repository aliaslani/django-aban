from decimal import ROUND_HALF_UP, Decimal

from django.db.models import F
from django.utils import timezone

from apps.core.exceptions import (
    DomainError,
    InsufficientStockError,
    ProductUnavailableError,
)

from .contracts import ProductRepository
from .dto import CartLine, PriceResult
from .models import Product
from .repositories import DjangoProductRepository


class PricingService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def calculate(self, lines: list[CartLine]) -> PriceResult:
        if not lines or len(lines) > 100:
            raise DomainError("Provide between 1 and 100 cart lines.")
        quantities = {}
        for line in lines:
            if type(line.quantity) is not int or not 1 <= line.quantity <= 1000:
                raise DomainError("Invalid quantity.")
            quantities[line.product_id] = (
                quantities.get(line.product_id, 0) + line.quantity
            )
        products = self.repository.get_many(list(quantities))
        subtotal = Decimal("0.00")
        for pk, quantity in quantities.items():
            product = products.get(pk)
            if product is None:
                raise ProductUnavailableError("Product unavailable.")
            if quantity > product.stock:
                raise InsufficientStockError("Insufficient stock.")
            subtotal += product.price * quantity
        discount = (
            subtotal * Decimal("0.10")
            if subtotal >= Decimal("1000.00")
            else Decimal("0.00")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return PriceResult(subtotal, discount, subtotal - discount)


class ProductService:
    @staticmethod
    def get_public_products():
        return DjangoProductRepository().list_active()


class InventoryService:
    @staticmethod
    def decrease_stock(product_id, quantity):
        if type(quantity) is not int or quantity <= 0:
            raise DomainError("Quantity must be positive.")
        updated = (
            Product.objects.active()
            .filter(pk=product_id, stock__gte=quantity)
            .update(stock=F("stock") - quantity, updated_at=timezone.now())
        )
        if not updated:
            raise InsufficientStockError("Product unavailable or insufficient stock.")
