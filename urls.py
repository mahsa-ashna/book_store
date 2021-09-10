from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from products.views import *

app_name = 'product'
urlpatterns = [
    # Template Views
    path('', ProductIndexView.as_view(), name='product_index_view'),
    path('Scientific/', ProductScientificView.as_view(), name='Scientific'),
    path('Historical/', ProductHistoricalView.as_view(), name='Historical'),
    path('Artistic/', ProductArtisticView.as_view(), name='Artistic'),
    path('product_card_view/<int:pk>', ProductCardView.as_view(), name='product_card_view'),
    path('product_detail/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('search_result/', SearchView.as_view(), name='search_result'),


    path('scookie', scookie),
    path('gcookie', gcookie),
    path('test_cookie', test_cookie),
    path('addcookie', addcookie),

   ]