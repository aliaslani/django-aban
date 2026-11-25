from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "price",
                    models.DecimalField(
                        max_digits=12,
                        decimal_places=2,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                ("stock", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["-created_at", "-pk"],
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(price__gte=Decimal("0.01")),
                        name="product_price_positive",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(stock__gte=0),
                        name="product_stock_nonnegative",
                    ),
                ],
            },
        )
    ]
