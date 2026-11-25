from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from apps.core.exceptions import DomainError
from apps.core.mixins import PageTitleMixin, StaffRequiredMixin

from .forms import PricingForm, ProductForm, ProductUpdateForm
from .models import Product
from .repositories import DjangoProductRepository
from .services import CartLine, PricingService, ProductService


class ProductBaseListView(PageTitleMixin, ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 20


class ProductListView(ProductBaseListView):
    page_title = "Products"

    def get_queryset(self):
        return ProductService.get_public_products()


class InactiveProductListView(
    StaffRequiredMixin, PermissionRequiredMixin, ProductBaseListView
):
    permission_required = "shop.view_product"
    page_title = "Inactive products"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class ProductDetailView(PageTitleMixin, DetailView):
    page_title = "Product details"
    model = Product
    template_name = "shop/product_detail.html"

    def get_queryset(self):
        return Product.objects.active()


class ProductCreateView(
    StaffRequiredMixin, PermissionRequiredMixin, PageTitleMixin, CreateView
):
    permission_required = "shop.add_product"
    page_title = "Create product"
    model = Product
    form_class = ProductForm
    template_name = "shop/product_form.html"
    success_url = reverse_lazy("product-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Product created.")
        return response


class ProductUpdateView(
    StaffRequiredMixin, PermissionRequiredMixin, PageTitleMixin, UpdateView
):
    permission_required = "shop.change_product"
    page_title = "Update product"
    model = Product
    form_class = ProductUpdateForm
    template_name = "shop/product_form.html"
    success_url = reverse_lazy("product-list")


class ProductPricingView(PageTitleMixin, FormView):
    page_title = "Calculate price"
    template_name = "shop/pricing.html"
    form_class = PricingForm

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product.objects.active(), pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(product=self.product, **kwargs)

    def form_valid(self, form):
        try:
            result = PricingService(DjangoProductRepository()).calculate(
                [CartLine(self.product.pk, form.cleaned_data["quantity"])]
            )
        except DomainError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        return self.render_to_response(self.get_context_data(form=form, result=result))
