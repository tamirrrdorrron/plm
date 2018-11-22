from django.urls import path

from . import views

urlpatterns = [

    path('', views.ProductListView.as_view(), name='ProductListView'),
    path('materials', views.MaterialListView.as_view(), name='MaterialListView'),
    path('materials/new', views.MaterialCreateView.as_view(), name='MaterialCreateView'),
    path('colours', views.ColourListView.as_view(), name='ColourListView'),
    path('colours/new', views.ColourCreateView.as_view(), name='ColourCreateView'),
    path('product/<int:pk>', views.ProductUpdateView.as_view(), name='ProductUpdateView'),
    path('product/<int:pk>/bom', views.ProductBomView.as_view(), name='ProductBomView'),
    path('product/<int:pk>/bom/modify', views.ProductBomCreateView.as_view(), name='ProductBomCreateView'),
    path('product/new', views.ProductCreateView.as_view(), name='ProductCreateView'),

]
