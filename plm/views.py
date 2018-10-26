from django.shortcuts import render, redirect
from .models import Designer, BOM, Material, Colourway
from .forms import ProductForm, SeasonalColourwayForm
from .helper import *


def index(request):
    products = Product.objects.all().order_by('id').reverse()
    designers = Designer.objects.all()
    if request.method == 'POST':
        selection = request.POST['list_designers']
        if selection != '0':
            products = products.filter(designer=selection)
    return render(request, 'plm/index.html', {'products': products, 'designers': designers})


def style(request, style_code):
    style_dict = get_style_code_dict(style_code)
    image = get_product_image(style_code)
    sc = get_seasonal_colourway_information(style_code)
    pi = get_product_information(style_code)
    return render(request, 'plm/style.html', {'productInfo': pi, 'seasonalColourways': sc, 'style_dict': style_dict, 'image': image})


def style_bom(request, style_code, bom_id):
    style_dict = get_style_code_dict(style_code)
    bom = BOM.objects.filter(id=bom_id).first()
    materials = bom.material.all()
    return render(request, 'plm/style_bom.html', {'materials': materials, 'style_dict': style_dict})


def materials(request):
    materials = Material.objects.all()
    return render(request, 'plm/materials.html', {'materials': materials})


def colourways(request):
    colourways = Colourway.objects.all()
    return render(request, 'plm/colourways.html', {'colourways': colourways})


def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('style', style_code=product.code)
    else:
        form = ProductForm()
    return render(request, 'plm/style_edit.html', {'form': form})


def seasonal_colourway_new(request, style_code):
    product_obj = Product.objects.filter(code=style_code)[0]
    if request.method == "POST":
        form = SeasonalColourwayForm(request.POST)
        if form.is_valid():
            seasonal_colourway = form.save(commit=False)
            seasonal_colourway.product = product_obj
            seasonal_colourway.save()
            return redirect('style', style_code=seasonal_colourway.product.code)
    else:
        form = SeasonalColourwayForm()
    return render(request, 'plm/seasonal_colourway_new.html', {'form': form})



# may be redundant soon..
# def style_colourway(request, style_code, colourway_id):
#     colourway = SeasonalColourway.objects.filter(id=colourway_id).values('colourway__name', 'season__name')[0]
#     styleDict = {'style_code': style_code}
#     bom = BOM.objects.filter(seasonal_colourway__product__code=style_code,
#                              seasonal_colourway__id = colourway_id
#                              ).values('seasonal_colourway__season__name',
#                                       'material__name',
#                                       'material__code',
#                                       'seasonal_colourway__product__code',
#                                       'seasonal_colourway__colourway__name'
#                                       )
#     return render(request, 'plm/style_colourway.html', {'bom': bom,
#                                                   'styleDict': styleDict,
#                                                   'colourway': colourway,
#                                                     'materials': materials})