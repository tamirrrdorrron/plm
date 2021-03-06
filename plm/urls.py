from django.urls import path

from . import views

urlpatterns = [

    path('', views.ProductListView.as_view(), name='ProductListView'),
    path('materials', views.MaterialListView.as_view(), name='MaterialListView'),
    path('materials/new', views.MaterialCreateView.as_view(), name='MaterialCreateView'),
    path('colours', views.ColourListView.as_view(), name='ColourListView'),
    path('colours/new', views.ColourCreateView.as_view(), name='ColourCreateView'),
    path('product/<int:pk>', views.ProductUpdateView.as_view(), name='ProductUpdateView'),
    path('product/<int:pk>/summary', views.ProductDetailView.as_view(), name='ProductDetailView'),
    path('product/<int:pk>/bom', views.ProductBomView.as_view(), name='ProductBomView'),
    path('product/<int:pk>/colours', views.ProductColoursListView.as_view(), name='ProductColoursListView'),
    path('product/<int:pk>/colours/new', views.ProductColoursCreateView.as_view(), name='ProductColoursCreateView'),
    path('product/<int:pk>/colours/<int:product_colour_pk>', views.ProductColoursUpdateView.as_view(),
         name='ProductColoursUpdateView'),
    path('product/<int:pk>/bom/<int:product_colour_pk>/delete', views.ProductColoursDeleteView.as_view(),
         name='ProductColoursDeleteView'),
    path('product/<int:pk>/bom/new', views.ProductBomCreateView.as_view(), name='ProductBomCreateView'),
    path('product/<int:pk>/bom/<int:bom_material_id_pk>', views.ProductBomUpdateView.as_view(), name='ProductBomUpdateView'),
    path('product/<int:pk>/bom/<int:bom_material_id_pk>/delete', views.ProductBomDeleteView.as_view(), name='ProductBomDeleteView'),
    path('product/<int:pk>/images', views.ImageListView.as_view(), name='ImageListView'),
    path('product/new', views.ProductCreateView.as_view(), name='ProductCreateView'),

]
