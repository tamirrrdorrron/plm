from django import forms
from .models import ProductColour, BOM, BOMMaterialComments


class ProductColourForm(forms.ModelForm):

    class Meta:
        model = ProductColour
        fields = ('season', 'colour')
        widgets = {
            'product': forms.HiddenInput(),
        }
#

class BOMForm(forms.ModelForm):

    class Meta:
        model = BOM
        fields = ('material',)
        widgets = {
            'product_colour': forms.HiddenInput(),
        }


class BOMMaterialCommentsForm(forms.ModelForm):

    class Meta:
        model = BOMMaterialComments
        fields = ('material', 'comment')
        widgets = {
            'bom': forms.HiddenInput(),
        }