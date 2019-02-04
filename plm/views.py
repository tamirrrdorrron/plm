from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse
from django.shortcuts import render, redirect
from plm.forms import MyForm
from django.forms import modelformset_factory, inlineformset_factory

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

        type_ref_images = models.ImageType.objects.filter(name='Reference Images').first()
        context['ref_images'] = models.Image.objects.filter(product=product, type=type_ref_images).all()

        type_construction_images = models.ImageType.objects.filter(name='Construction Images').first()
        context['construction_images'] = models.Image.objects.filter(product=product, type=type_construction_images).all()

        type_colourway_images = models.ImageType.objects.filter(name='Colourway Images').first()
        context['colourway_images'] = models.Image.objects.filter(product=product, type=type_colourway_images).all()

        return context


class ProductColoursCreateView(CreateView):
    fields = ('colour',
              'season',
              'comment'
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


class ProductColoursUpdateView(UpdateView):
    fields = ('colour',
              'season',
              'comment'
              )
    model = models.ColourSeason

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['base_template'] = 'plm/base_product.html'
        return context

    def get_object(self):
        return models.ColourSeason.objects.filter(pk=self.kwargs['product_colour_pk']).first()

    def get_success_url(self):
        return reverse('ProductColoursListView', kwargs={'pk': self.kwargs['pk']})


class ProductColoursDeleteView(DeleteView):
    model = models.ColourSeason

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        context['base_template'] = 'plm/base_product.html'
        return context

    def get_object(self):
        return models.ColourSeason.objects.filter(pk=self.kwargs['product_colour_pk']).first()

    def get_success_url(self):
        return reverse('ProductColoursListView', kwargs={'pk': self.kwargs['pk']})


class ImageListView(ListView):
    model = models.Image
    context_object_name = 'images'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_template'] = 'plm/base_product.html'
        context['product'] = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        return context

    def get_queryset(self):
        product = models.Product.objects.filter(pk=self.kwargs['pk']).first()
        data = models.Image.objects.filter(product=product).all()
        return data


def ProductMeasurementChart(request, pk):

    product = models.Product.objects.filter(pk=pk).first()
    measurement_chart = models.MeasurementChart.objects.filter(product=product).first()
    size_header = measurement_chart.size_header.size.all()

    fields = ['code', 'name', 'sort']

    POMFormSet = modelformset_factory(models.POM, fields=fields, extra=1)

    if request.method == "POST":
        formset_pom = POMFormSet(request.POST, request.FILES)
        print(formset_pom.errors)
        # for i in formset_pom:
        #     print(i.cleaned_data['measurement'])
        if formset_pom.is_valid():
            instances = formset_pom.save(commit=False)
            for instance in instances:
                instance.measurement_chart = measurement_chart
                instance.save()
            return redirect('ProductMeasurementChart', pk=product.pk)

    else:
        formset_pom = POMFormSet(queryset=models.POM.objects.filter(measurement_chart=measurement_chart))

    return render(request, 'plm/measurementchart_detail.html', {'formset_pom': formset_pom,
                                                                'product': product,
                                                                'size_header': size_header,})









# below code is a function to set default values to a POM sizes measurements
def add_pom(name, code, measurement_chart):
    pom = models.POM(name=name, code=code, measurement_chart=measurement_chart)
    pom.save()
    sizes = [x for x in measurement_chart.size_header.size.all()]
    for size in sizes:
        pom_measurement = models.POMMeasurement(size=size, measurement='0.00')
        pom_measurement.save()
        pom.measurement.add(pom_measurement)


def update_pom_measurement_by_size(product_pk, pom_code, size, measurement):
    product = models.Product.objects.filter(pk=product_pk).first()
    measurement_chart = models.MeasurementChart.objects.filter(product=product).first()
    size = models.Size.objects.filter(size=size).first()

    pom = models.POM.objects.filter(code=pom_code, measurement_chart=measurement_chart).first()
    pom_measurement = pom.measurement.filter(size=size).first()
    pom_measurement.measurement = measurement
    pom_measurement.save()