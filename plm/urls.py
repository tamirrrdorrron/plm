from django.urls import path
from .views import product_bom
from . import views


urlpatterns = [

    path('', views.ProductListView.as_view(), name='ProductListView'),
    path('materials', views.MaterialListView.as_view(), name='MaterialListView'),
    path('colours', views.ColourListView.as_view(), name='ColourListView'),
    path('product/<int:pk>', views.ProductUpdateView.as_view(), name='ProductUpdateView'),
    path('product/<int:pk>/colours', views.ProductColourListView.as_view(), name='ProductColourListView'),
    path('product/<int:pk>/colour/new', views.ProductColourCreateView.as_view(), name='ProductColourCreateView'),
    path('product/<str:pk_product>/bom/<str:pk_bom>', product_bom, name='product_bom'),
    path('product/new', views.ProductCreateView.as_view(), name='ProductCreateView'),

]
