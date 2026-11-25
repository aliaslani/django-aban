from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.shop.models import Product


class ViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Hidden", price="20.00", is_active=False
        )

    def test_hidden_product(self):
        response = self.client.get(reverse("product-detail", args=[self.product.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertIn("X-Request-ID", response)

    def test_anonymous_create(self):
        self.assertEqual(self.client.get(reverse("product-create")).status_code, 302)

    def test_customer_create(self):
        user = get_user_model().objects.create_user(username="customer")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("product-create")).status_code, 403)

    def test_superuser_create(self):
        user = get_user_model().objects.create_superuser(
            username="admin", password="test-password-123"
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse("product-create"),
            {"name": "Keyboard", "price": "75.00", "stock": 20, "is_active": "on"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name="Keyboard").exists())
