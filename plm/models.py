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


class Season(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    code = models.CharField(max_length=30, unique=True)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(max_length=1000)
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
    photo = models.ImageField(upload_to='materials')

    def __str__(self):
        return self.name


class ProductColour(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    colour = models.ForeignKey(Colour, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("product", "season", "colour")

    def __str__(self):
        return "%s %s %s" % (self.product, self.season, self.colour)


class BOM(models.Model):
    name = models.CharField(max_length=100, blank=True)
    material = models.ManyToManyField(Material, blank=True, through='BOMMaterialComments')
    product_colour = models.ForeignKey(ProductColour, on_delete=models.PROTECT)

    def __str__(self):
        return "%s %s %s %s" % (self.product_colour.product,
                                self.product_colour.season,
                                self.product_colour.colour,
                                self.name
                                )


class BOMMaterialComments(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    bom = models.ForeignKey(BOM, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return self.comment

