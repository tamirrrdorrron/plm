from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Designer, Colour, BOMMaterialComments
from . import models
from .forms import BOMMaterialCommentsForm
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
        context['base_template'] = 'plm/base_product.html'
        context['product'] = Product.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def get_queryset(self):
        data = self.model.objects.filter(product=self.kwargs['pk']).all()
        return data


class ProductColourCreateView(CreateView):
    fields = ('colour', 'season')
    model = models.ProductColour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base_product.html'
        context['product'] = Product.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        object_product = Product.objects.filter(pk=self.kwargs['pk']).first()
        self.object.product = object_product
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


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