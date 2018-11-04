from django import forms
from .models import Product, ProductColour, BOM


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('code',
                  'short_description',
                  'long_description',
                  'designer',
                  'production_coordinator',
                  'pattern_maker',
                  'photo',)


class ProductColourForm(forms.ModelForm):

    class Meta:
        model = ProductColour
        fields = ('season', 'colour')
        widgets = {
            'product': forms.HiddenInput(),
        }


class BOMForm(forms.ModelForm):

    class Meta:
        model = BOM
        fields = ('material',)
        widgets = {
            'product_colour': forms.HiddenInput(),
        }