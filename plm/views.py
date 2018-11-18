from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView

from . import models


class ProductListView(ListView):
    context_object_name = 'products'
    model = models.Product
    ordering = ['-id']


class MaterialListView(ListView):
    context_object_name = 'materials'
    model = models.Material
    ordering = ['-id']


class MaterialCreateView(CreateView):
    fields = ('code',
              'name',
              'photo'
              )
    model = models.Material

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base.html'
        return context


class ColourListView(ListView):
    context_object_name = 'colours'
    model = models.Colour
    ordering = ['-id']


class ColourCreateView(CreateView):
    fields = ('code',
              'name'
              )
    model = models.Colour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base.html'
        return context


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
        context['product'] = models.Product.objects.filter(pk=self.object.id).first()
        context['base_template'] = 'plm/base_product.html'
        return context


class ProductColourListView(ListView):
    context_object_name = 'colours'
    model = models.ProductColour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base_product.html'
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
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
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        object_product = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        self.object.product = object_product
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


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


class ProductBomListView(ListView):
    context_object_name = 'boms'
    template_name = 'plm/productbom_list.html'
    model = models.BOM

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base_product.html'
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def get_queryset(self):
        pc = models.ProductColour.objects.filter(product=self.kwargs['pk']).values('pk')
        data = self.model.objects.filter(product_colour__in=pc).all()
        return data


class ProductBomMaterialListView(ListView):
    context_object_name = 'bommaterials'
    template_name = 'plm/productbommaterials_list.html'
    model = models.BOMMaterialComments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base_product.html'
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['bom'] = models.BOM.objects.filter(pk=self.kwargs['bom_pk']).first()
        return context

    def get_queryset(self):
        data = self.model.objects.filter(bom=self.kwargs['bom_pk']).all()
        return data


class ProductBomCreateView(CreateView):
    fields = ('name',
              'product_colour'
              )
    model = models.BOM
    template_name = 'plm/productbom_form.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base_product.html'
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        return context


class ProductBomMaterialCreateView(CreateView):
    fields = ('material',
              'comment'
              )
    model = models.BOMMaterialComments
    template_name = 'plm/productbommaterialadd_form.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base_product.html'
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['bom'] = models.BOM.objects.filter(pk=self.kwargs['bom_pk']).first()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        object_bom = models.BOM.objects.filter(pk=self.kwargs['bom_pk']).first()
        self.object.bom = object_bom
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
