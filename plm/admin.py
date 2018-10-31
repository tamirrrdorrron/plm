from django.contrib import admin
from plm.models import Product, Designer, ProductionCoordinator, PatternMaker, Colourway, Season, StyleColourway, Material, BOM

# Register your models here.

admin.site.register(Colourway)
admin.site.register(Product)
admin.site.register(Designer)
admin.site.register(ProductionCoordinator)
admin.site.register(PatternMaker)
admin.site.register(Season)
admin.site.register(StyleColourway)
admin.site.register(Material)
admin.site.register(BOM)