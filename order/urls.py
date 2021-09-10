from django.urls import path

from order.views import *

app_name = 'order'
urlpatterns = [
    path('cart_list', CartList.as_view(), name='cart_list'),
    path('cart_delete/<int:pk>', DeleteCartItem.as_view(), name='cart_delete'),
    path('plus_product_qty/<o_i_id>', plus_product_qty, name='plus_product_qty'),
    path('minus_product_qty/<o_i_id>', minus_product_qty, name='minus_product_qty'),


]
