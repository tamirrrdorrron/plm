from django.urls import path
from .views import index, product, materials, colours, product_new, product_colour_new, product_bom


urlpatterns = [
    path('', index, name='index'),
    path('materials', materials, name='materials'),
    path('colours', colours, name='colours'),
    path('product/<int:pk_product>', product, name='product'),
    path('product/<int:pk_product>/colour/new', product_colour_new, name='product_colour_new'),
    path('product/<str:pk_product>/bom/<str:pk_bom>', product_bom, name='product_bom'),
    path('product/new', product_new, name='product_new'),
]