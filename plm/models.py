from django.db import models


class Material(models.Model):
    code = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255)
    colour = models.CharField(max_length=100)

    def __str__(self):
        return "%s %s %s" % (self.code, self.description, self.colour)


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


class Product(models.Model):
    code = models.CharField(max_length=30, unique=True)
    short_description = models.CharField(max_length=255)
    long_description = models.CharField(max_length=1000)
    material = models.ManyToManyField(Material)
    designer = models.ForeignKey(Designer, on_delete=models.PROTECT)
    production_coordinator = models.ForeignKey(ProductionCoordinator, on_delete=models.PROTECT)
    pattern_maker = models.ForeignKey(PatternMaker, on_delete=models.PROTECT)

    def __str__(self):
        return "%s %s" % (self.code, self.short_description)