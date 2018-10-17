from django.shortcuts import render
from .models import Product, Designer, SeasonalColourway, BOM, Material, Colourway


def index(request):
    products = Product.objects.all()
    designers = Designer.objects.all()
    if request.method == 'POST':
        selection = request.POST['list_designers']
        if selection != '0':
            products = products.filter(designer=selection)
    return render(request, 'plm/index.html', {'products': products, 'designers': designers})


def style(request, style_code):
    sc = SeasonalColourway.objects.filter(product__code=style_code).values('id',
                                                                           'colourway__name',
                                                                           'season__name',
                                                                           'product__code')
    pi = Product.objects.filter(code=style_code).values(
        'code',
        'short_description',
        'designer__name',
        'production_coordinator__name',
        'pattern_maker__name'
    )
    styleDict = {'style_code': style_code}
    return render(request, 'plm/style.html', {'productInfo': pi, 'seasonalColourways': sc, 'styleDict': styleDict})


def style_colourway(request, style_code, colourway_id):
    colourway = SeasonalColourway.objects.filter(id=colourway_id).values('colourway__name', 'season__name')[0]
    styleDict = {'style_code': style_code}
    bom = BOM.objects.filter(seasonal_colourway__product__code=style_code,
                             seasonal_colourway__id = colourway_id
                             ).values('seasonal_colourway__season__name',
                                      'material__name',
                                      'material__code',
                                      'seasonal_colourway__product__code',
                                      'seasonal_colourway__colourway__name'
                                      )
    return render(request, 'plm/style_colourway.html', {'bom': bom,
                                                  'styleDict': styleDict,
                                                  'colourway': colourway}
                  )


def materials(request):
    materials = Material.objects.all()
    return render(request, 'plm/materials.html', {'materials': materials})


def colourways(request):
    colourways = Colourway.objects.all()
    return render(request, 'plm/colourways.html', {'colourways': colourways})

