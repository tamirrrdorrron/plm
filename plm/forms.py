from django import forms
from .models import Product, SeasonalColourway


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


class SeasonalColourwayForm(forms.ModelForm):

    class Meta:
        model = SeasonalColourway
        fields = ('season', 'colourway')
        widgets = {
            'product': forms.HiddenInput(),
        }