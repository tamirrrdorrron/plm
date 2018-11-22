from django.db import models
from django.urls import reverse


class Designer(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return "%s" % self.name


class PatternMaker(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return "%s" % self.name


class ProductionCoordinator(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return "%s" % self.name


class Colour(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ColourListView')


class Season(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=30, unique=True)
    short_description = models.CharField(max_length=255)
    designer = models.ForeignKey(Designer, on_delete=models.PROTECT)
    production_coordinator = models.ForeignKey(ProductionCoordinator, on_delete=models.PROTECT)
    pattern_maker = models.ForeignKey(PatternMaker, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='styles', default='styles/main.JPG')

    def __str__(self):
        return "%s %s" % (self.code, self.short_description)

    def get_absolute_url(self):
        return reverse('ProductUpdateView', kwargs={'pk': self.pk})


class Material(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='materials', default='materials/main.JPG')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('MaterialListView')


class BOM(models.Model):
    name = models.CharField(max_length=100, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    season = models.ForeignKey(Season, on_delete=models.PROTECT, blank=True, null=True)
    colour = models.ManyToManyField(Colour, blank=True)
    material = models.ManyToManyField(Material, blank=True, through='BOMMaterialComments')

    def __str__(self):
        return "%s %s" % (self.product.code,
                          self.colour.name)

    def get_absolute_url(self):
        return reverse('ProductBomView', kwargs={'pk': self.product.pk})


class BOMMaterialComments(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('ProductBomView', kwargs={'pk': self.bom.product.pk})
