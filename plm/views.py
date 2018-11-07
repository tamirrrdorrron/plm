from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Designer, Colour
from .forms import ProductForm, ProductColourForm, BOMForm
from .helper import *


def index(request):
    products = Product.objects.all().order_by('pk').reverse()
    designers = Designer.objects.all()
    if request.method == 'POST':
        selection = request.POST['list_designers']
        if selection != '0':
            products = products.filter(designer=selection)
    return render(request, 'plm/index.html', {'products': products, 'designers': designers})


def materials(request):
    materials = Material.objects.all()
    return render(request, 'plm/materials.html', {'materials': materials})


def colours(request):
    colours = Colour.objects.all()
    return render(request, 'plm/colours.html', {'colours': colours})


def product(request, pk_product):
    product = get_product_dict(pk_product)
    product_colours = get_product_colour_information(pk_product)
    product_instance = get_object_or_404(Product, pk=pk_product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product_instance)
        if form.is_valid():
            form.save()
    else:
        form = ProductForm(instance=product_instance)
    return render(request, 'plm/product.html', {'product': product, 'product_colours': product_colours, 'form': form})


def product_colour_new(request, pk_product):
    product = get_product_dict(pk_product)
    if request.method == "POST":
        form = ProductColourForm(request.POST)
        if form.is_valid():
            product_colour = form.save(commit=False)
            product_colour.product = product
            product_colour.save()
            bom = BOM(product_colour=product_colour)
            bom.save()
            bom_pk = bom.pk
            return redirect('product_bom', pk_product=pk_product, pk_bom=bom_pk)
    else:
        form = ProductColourForm()
    return render(request, 'plm/product_colour_new.html', {'form': form, 'product': product})


def product_bom(request, pk_product, pk_bom):
    product = get_product_dict(pk_product)
    bom = BOM.objects.filter(pk=pk_bom).first()
    materials = bom.material.all()
    if request.method == "POST":
        if not 'pk_material' in request.POST.keys():
            form = BOMForm(request.POST)
            product_colour = BOM.objects.filter(pk=pk_bom).first().product_colour
            if form.is_valid():
                update_bom(form, product_colour, pk_bom)
                return redirect('product_bom', pk_product=pk_product, pk_bom=pk_bom)
        elif 'pk_material' in request.POST.keys():
            pk_material = request.POST['pk_material']
            remove_material_from_bom(pk_bom=pk_bom, pk_material=pk_material)
            return redirect('product_bom', pk_product=pk_product, pk_bom=pk_bom)
    else:
        form = BOMForm()
    return render(request, 'plm/product_bom.html', {'product': product, 'materials': materials, 'form': form, 'bom': bom})


def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('product', pk_product=product.pk)
    else:
        form = ProductForm()
    return render(request, 'plm/product_edit.html', {'form': form})

