from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ProductDTO:
    id: int
    name: str
    price: Decimal
    stock: int


@dataclass(frozen=True)
class CartLine:
    product_id: int
    quantity: int


@dataclass(frozen=True)
class PriceResult:
    subtotal: Decimal
    discount: Decimal
    total: Decimal
