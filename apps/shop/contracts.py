from typing import Protocol

from .dto import ProductDTO


class ProductRepository(Protocol):
    def get_many(self, ids: list[int]) -> dict[int, ProductDTO]: ...
