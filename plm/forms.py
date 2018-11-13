from django import forms
from .models import BOM, BOMMaterialComments


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