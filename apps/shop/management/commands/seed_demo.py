from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.shop.models import Product


class Command(BaseCommand):
    help = "Create classroom sample products without overwriting existing records."

    def handle(self, *args, **options):
        for name, price, stock, active in [
            ("Laptop", "1200.00", 10, True),
            ("Keyboard", "75.00", 20, True),
            ("Monitor", "250.00", 0, True),
            ("Old Laptop", "500.00", 0, False),
        ]:
            if not Product.objects.filter(name=name).exists():
                Product.objects.create(
                    name=name, price=Decimal(price), stock=stock, is_active=active
                )
        self.stdout.write(self.style.SUCCESS("Demo products ready."))
