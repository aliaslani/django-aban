from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
    path("inactive/", views.InactiveProductListView.as_view(), name="product-inactive"),
    path("create/", views.ProductCreateView.as_view(), name="product-create"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product-update"),
    path("<int:pk>/price/", views.ProductPricingView.as_view(), name="product-price"),
]
