from django.urls import path
from .views import index, style, style_colourway, materials, colourways, product_new, seasonal_colourway_new


urlpatterns = [
    path('', index, name='index'),
    path('materials', materials, name='materials'),
    path('colourways', colourways, name='colourways'),
    path('style/<str:style_code>', style, name='style'),
    path('style/<str:style_code>/seasonal_colourway_new', seasonal_colourway_new, name='seasonal_colourway_new'),
    path('style/<str:style_code>/colourway/<str:colourway_id>', style_colourway, name='style_colourway'),
    path('new/style', product_new, name='product_new'),
]