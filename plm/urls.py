from django.urls import path
from .views import index, style, materials, colourways, product_new, style_colourway_new, style_bom


urlpatterns = [
    path('', index, name='index'),
    path('materials', materials, name='materials'),
    path('colourways', colourways, name='colourways'),
    path('style/<str:style_code>', style, name='style'),
    path('style/<str:style_code>/style_colourway_new', style_colourway_new, name='style_colourway_new'),
    path('style/<str:style_code>/bom/<str:bom_id>', style_bom, name='style_bom'),
    path('new/style', product_new, name='product_new'),
]