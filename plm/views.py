from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse
from plm.forms import MyForm

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
              'content',
              'weight',
              'vendor_mill',
              'vendor_ref',
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
              'name',
              'notes'
              )
    model = models.Colour

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base.html'
        return context


class ProductUpdateView(UpdateView):
    form_class = MyForm
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = models.Product.objects.filter(pk=self.object.id).first()
        context['bom'] = models.BOM.objects.filter(product=self.object).first()
        context['base_template'] = 'plm/base_product.html'
        return context


class ProductCreateView(CreateView):
    fields = ('code',
              'short_description',
              'designer',
              'production_coordinator',
              'pattern_maker',
              'instructions',
              'photo'
              )
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base.html'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        product = self.object
        create_bom = models.BOM(name='BOM', product=product)
        create_bom.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductBomView(ListView):
    context_object_name = 'materials'
    template_name = 'plm/productbommaterials_list.html'
    model = models.BOMMaterialComments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base_product.html'
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def get_queryset(self):
        product = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        bom = models.BOM.objects.filter(product=product).first()
        data = models.BOMMaterialComments.objects.filter(bom=bom).all()
        return data


class ProductBomCreateView(CreateView):
    fields = ('material',
              'comment'
              )
    template_name = 'plm/productbommaterial_form.html'
    model = models.BOMMaterialComments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['base_template'] = 'plm/base_product.html'
        return context

    def get_queryset(self):
        product = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        bom = models.BOM.objects.filter(product=product).first()
        data = models.BOMMaterialComments.objects.filter(bom=bom).all()
        return data

    def form_valid(self, form):
        product = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        bom = models.BOM.objects.filter(product=product).first()
        self.object = form.save(commit=False)
        self.object.bom = bom
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductBomUpdateView(UpdateView):
    fields = ('material',
              'comment'
              )
    template_name = 'plm/productbommaterial_form.html'
    model = models.BOMMaterialComments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['base_template'] = 'plm/base_product.html'
        return context

    def get_object(self):
        return models.BOMMaterialComments.objects.filter(pk=self.kwargs['bom_material_id_pk']).first()


class ProductBomDeleteView(DeleteView):
    model = models.BOMMaterialComments
    template_name = 'plm/productbommaterial_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['base_template'] = 'plm/base_product.html'
        return context

    def get_object(self):
        return models.BOMMaterialComments.objects.filter(pk=self.kwargs['bom_material_id_pk']).first()

    def get_success_url(self):
        return reverse('ProductBomView', kwargs={'pk': self.kwargs['pk']})


class ProductDetailView(DetailView):
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base_product.html'
        product = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        bom = models.BOM.objects.filter(product=product).first()
        context['bom_materials'] = models.BOMMaterialComments.objects.filter(bom=bom)
        context['colours'] = models.ColourSeason.objects.filter(product=product).all()
        return context


class ProductColoursCreateView(CreateView):
    fields = ('colour',
              'season'
              )
    model = models.ColourSeason

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['base_template'] = 'plm/base_product.html'
        return context

    def form_valid(self, form):
        product = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        self.object = form.save(commit=False)
        self.object.product = product
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductColoursListView(ListView):
    context_object_name = 'productcolours'
    model = models.ColourSeason

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['base_template'] = 'plm/base_product.html'
        return context

    def get_queryset(self):
        product = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        data = models.ColourSeason.objects.filter(product=product).all()
        return data

