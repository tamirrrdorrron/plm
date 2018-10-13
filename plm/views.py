from django.shortcuts import render
from .models import Product, Designer, SeasonalColourway


def index(request):
    qs = Product.objects.all()
    designers = Designer.objects.all()
    if request.method == 'POST':
        selection = request.POST['list_designers']
        if selection != '0':
            qs = qs.filter(designer=selection)
    return render(request, 'plm/index.html', {'qs': qs, 'designers': designers})


def style(request, style_code):
    sc = SeasonalColourway.objects.filter(product__code=style_code).values('colourway__name', 'season__name')
    pi = Product.objects.filter(code=style_code).values(
        'code',
        'short_description',
        'designer__name',
        'production_coordinator__name',
        'pattern_maker__name'
    )
    return render(request, 'plm/style.html', {'productInfo': pi, 'seasonalColourways': sc})
