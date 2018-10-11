from django.urls import path, include
from .views import index, style


urlpatterns = [
    path('', index, name='index'),
    path('style/<str:style_code>', style, name='style'),
 ]
