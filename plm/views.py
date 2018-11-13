from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Designer, Colour, BOMMaterialComments
from . import models
from .forms import ProductColourForm, BOMMaterialCommentsForm
from .helper import *


class ProductListView(ListView):
    context_object_name = 'products'
    model = models.Product

    ordering = ['-id']


class MaterialListView(ListView):
    context_object_name = 'materials'
    model = models.Material


class ColourListView(ListView):
    context_object_name = 'colours'
    model = models.Colour


class ProductUpdateView(UpdateView):
    fields = ('code',
              'short_description',
              'long_description',
              'designer',
              'production_coordinator',
              'pattern_maker'
              )
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.filter(pk=self.object.id).first()
        context['base_template'] = 'plm/base_product.html'
        return context


class ProductColourListView(ListView):
    context_object_name = 'colours'
    model = models.ProductColour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def get_queryset(self):
        data = self.model.objects.filter(product=self.kwargs['pk']).all()
        return data


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
    materials = BOMMaterialComments.objects.filter(bom=bom)
    if request.method == "POST":
        if not 'pk_material' in request.POST.keys():
            form = BOMMaterialCommentsForm(request.POST)
            product_colour = BOM.objects.filter(pk=pk_bom).first().product_colour
            if form.is_valid():
                update_bom(form, product_colour, pk_bom)
                return redirect('product_bom', pk_product=pk_product, pk_bom=pk_bom)
        elif 'pk_material' in request.POST.keys():
            pk_material = request.POST['pk_material']
            remove_material_from_bom(pk_bom=pk_bom, pk_material=pk_material)
            return redirect('product_bom', pk_product=pk_product, pk_bom=pk_bom)
    else:
        form = BOMMaterialCommentsForm()
    return render(request, 'plm/product_bom.html', {'product': product, 'materials': materials, 'form': form, 'bom': bom})


class ProductCreateView(CreateView):
    fields = ('code',
              'short_description',
              'long_description',
              'designer',
              'production_coordinator',
              'pattern_maker',
              'photo'
              )
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base.html'
        return context



# def product(request, pk_product):
#     product = get_product_dict(pk_product)
#     product_colours = get_product_colour_information(pk_product)
#     product_instance = get_object_or_404(Product, pk=pk_product)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, instance=product_instance)
#         if form.is_valid():
#             form.save()
#     else:
#         form = ProductForm(instance=product_instance)
#     return render(request, 'plm/product.html', {'product': product, 'product_colours': product_colours, 'form': form})
