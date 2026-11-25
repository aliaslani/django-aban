from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "is_active"]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError("Name must have at least three characters.")
        return name


class ProductUpdateForm(ProductForm):
    class Meta(ProductForm.Meta):
        fields = ["name", "description", "price", "is_active"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save(update_fields=[*self.Meta.fields, "updated_at"])
        return instance


class PricingForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=1000)
