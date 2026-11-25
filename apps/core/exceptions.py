class DomainError(Exception):
    code = "domain_error"

    def __init__(self, message, *, details=None):
        super().__init__(message)
        self.details = details or {}


class ProductUnavailableError(DomainError):
    code = "product_unavailable"


class InsufficientStockError(DomainError):
    code = "insufficient_stock"
