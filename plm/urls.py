from django.urls import path
from .views import index, style, colourway


urlpatterns = [
    path('', index, name='index'),
    path('style/<str:style_code>', style, name='style'),
    path('style/<str:style_code>/colourway/<str:colourway_id>', colourway, name='colourway')
 ]
