from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.views.decorators.http import require_POST
# from order.cart import Cart
# from order.forms import CartAddProductForm
from rest_framework import generics

from order.models import Order, OrderItem
from products.models import Product


class CartList(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # user = User.objects.get(id=request.user.id)
        user = request.user
        if user.address_set.count() == 0:
            return redirect(reverse_lazy('customer:address_create'))
        # items = list(request.COOKIES.get('cart', '').split('-')[:-1])
        items = set(request.COOKIES.get('cart', '').split('-')[:-1])
        order = user.order_set.filter(status__exact='Pr')
        # print(order)
        if order:
            if order.count() == 1:
                # order = order
                order = order.first()
                # print('order: ', order, 'items: ', items)
                for item in items:
                    product = Product.objects.get(id=int(item))
                    if not order.orders.filter(product=product):
                        OrderItem.objects.create(order=order, product=product)



        else:
            new_order = Order.objects.create(user=user)
            order = new_order
            # print('new order: ', order, 'items: ', items)
            for item in items:
                product = Product.objects.get(id=int(item))
                OrderItem.objects.create(order=order, product=product)

        cart_items = order.orders.all()
        # print(cart_items.count())
        resp = render(request, 'order_temp/detail.html', {
            'order': order,
            'cart_items': cart_items,
            'n': list(range(cart_items.count()))
        })
        resp.set_cookie('cart', '')
        return resp

# Plus product qty
def plus_product_qty(request, o_i_id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    if request.method == 'GET':
        return reverse_lazy('order:cart_list')

    # fetch the object related to passed id
    obj = get_object_or_404(OrderItem, id=o_i_id)

    if request.method == "POST":
        # add object
        if obj.number < obj.product.leftovers:
            obj.number = F('number') + 1
            obj.save()
        return HttpResponseRedirect(reverse_lazy('order:cart_list'))

        return render(request, "order_temp/detail.html", context)



# Minus product qty
def minus_product_qty(request, o_i_id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    if request.method == 'GET':
        return reverse_lazy('order:cart_list')

    # fetch the object related to passed id
    obj = get_object_or_404(OrderItem, id=o_i_id)

    if request.method == "POST":
        # add object
        if obj.number > 1:
            obj.number = F('number') - 1
            obj.save()
        return HttpResponseRedirect(reverse_lazy('order:cart_list'))

        return render(request, "order_temp/detail.html", context)


# Delete from cart
class DeleteCartItem(LoginRequiredMixin, generic.DeleteView):
    model = OrderItem
    success_url = reverse_lazy('order:cart_list')


