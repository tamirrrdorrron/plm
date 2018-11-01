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


class Material(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='materials')

    def __str__(self):
        return self.name


class StyleColourway(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    colourway = models.ForeignKey(Colourway, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("product", "season", "colourway")

    def __str__(self):
        return "%s %s %s" % (self.product, self.season, self.colourway)


class BOM(models.Model):
    name = models.CharField(max_length=100, blank=True)
    material = models.ManyToManyField(Material, blank=True)
    style_colourway = models.ForeignKey(StyleColourway, on_delete=models.PROTECT)

    def __str__(self):
        return "%s %s %s %s" % (self.style_colourway.product,
                                self.style_colourway.season,
                                self.style_colourway.colourway,
                                self.name
                                )
