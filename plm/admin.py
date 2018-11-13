from django.contrib import admin
from plm.models import Product, Designer, ProductionCoordinator, PatternMaker, Colour, Season, ProductColour, Material, BOM, BOMMaterialComments

# Register your models here.

admin.site.register(Colour)
admin.site.register(Product)
admin.site.register(Designer)
admin.site.register(ProductionCoordinator)
admin.site.register(PatternMaker)
admin.site.register(Season)
admin.site.register(ProductColour)
admin.site.register(Material)
admin.site.register(BOM)
admin.site.register(BOMMaterialComments)