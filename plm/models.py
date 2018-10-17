from django.db import models


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


class Colourway(models.Model):
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
    long_description = models.CharField(max_length=1000)
    designer = models.ForeignKey(Designer, on_delete=models.PROTECT)
    production_coordinator = models.ForeignKey(ProductionCoordinator, on_delete=models.PROTECT)
    pattern_maker = models.ForeignKey(PatternMaker, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='styles')

    def __str__(self):
        return "%s %s" % (self.code, self.short_description)


class SeasonalColourway(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    colourway = models.ForeignKey(Colourway, on_delete=models.PROTECT)

    def __str__(self):
        return "%s %s %s" % (self.product, self.season, self.colourway)


class Material(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='materials')

    def __str__(self):
        return self.name


class BOM(models.Model):
    material = models.ManyToManyField(Material)
    seasonal_colourway = models.ForeignKey(SeasonalColourway, on_delete=models.PROTECT)

    def __str__(self):
        return "%s %s %s" % (self.seasonal_colourway.product,
                             self.seasonal_colourway.season,
                             self.seasonal_colourway.colourway
                             )