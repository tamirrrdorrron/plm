from django import forms
from .models import Product, StyleColourway, BOM


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


class StyleColourwayForm(forms.ModelForm):

    class Meta:
        model = StyleColourway
        fields = ('season', 'colourway')
        widgets = {
            'product': forms.HiddenInput(),
        }


class BOMForm(forms.ModelForm):

    class Meta:
        model = BOM
        fields = ('material',)
        widgets = {
            'style_colourway': forms.HiddenInput(),
        }