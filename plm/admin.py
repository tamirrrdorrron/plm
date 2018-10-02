from django.contrib import admin
from plm.models import Product, Material, Designer, ProductionCoordinator, PatternMaker

# Register your models here.


admin.site.register(Product)
admin.site.register(Material)
admin.site.register(Designer)
admin.site.register(ProductionCoordinator)
admin.site.register(PatternMaker)