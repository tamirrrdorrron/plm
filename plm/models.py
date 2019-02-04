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
    notes = models.CharField(max_length=255, blank=True)

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
    colour = models.ManyToManyField(Colour, blank=True, through='ColourSeason')
    instructions = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return "%s %s" % (self.code, self.short_description)

    def get_absolute_url(self):
        return reverse('ProductUpdateView', kwargs={'pk': self.pk})


class ColourSeason(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    colour = models.ForeignKey(Colour, on_delete=models.PROTECT)
    season = models.ForeignKey(Season, on_delete=models.PROTECT, blank=True)
    comment = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('colour', 'season', 'product')

    def __str__(self):
        return "%s %s %s" % (self.product, self.colour, self.season)

    def get_absolute_url(self):
        return reverse('ProductColoursListView', kwargs={'pk': self.product.pk})


class Material(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    content = models.CharField(max_length=255, blank=True)
    weight = models.CharField(max_length=255, blank=True)
    vendor_mill = models.CharField(max_length=255, blank=True)
    vendor_ref = models.CharField(max_length=255, blank=True)
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


class ImageType(models.Model):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='ref_images')
    type = models.ForeignKey(ImageType, on_delete=models.PROTECT, blank=False)
    comment = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return "%s %s" % (self.product, self.type)


class Size(models.Model):
    size = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.size


class SizeHeader(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    size = models.ManyToManyField(Size, blank=False)

    def __str__(self):
        return self.name


class MeasurementChart(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    size_header = models.ForeignKey(SizeHeader, on_delete=models.PROTECT)

    def __str__(self):
        return "%s %s" % (self.product.code, self.size_header.name)


class POM(models.Model):
    measurement_chart = models.ForeignKey(MeasurementChart, blank=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=50, blank=True)
    sort = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return "%s %s" % (self.name, self.code)


class POMMeasurement(models.Model):
    size = models.ForeignKey(Size, blank=False, on_delete=models.PROTECT)
    measurement = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, blank=False)
    pom = models.ForeignKey(POM, blank=False, on_delete=models.PROTECT)

    def __str__(self):
        return "Size %s - measurement: %s cm" % (
            self.size,
            self.measurement
        )