from django import forms
from plm.models import Product


class MyForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('code',
                  'short_description',
                  'designer',
                  'production_coordinator',
                  'pattern_maker',
                  'instructions'
                  )
        widgets = {
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'id': 'exampleFormControlTextarea1', 'rows': '5'}),
        }