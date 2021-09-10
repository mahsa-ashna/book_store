from django.shortcuts import render

# Create your views here.
from django.views import generic

from products.models import Product
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import generic
# Create your views here.
from rest_framework import generics
from django.utils.translation import gettext_lazy as _

from products.models import Product


class Landing(generic.TemplateView):
    template_name = 'landing_temp/landing.html'
    extra_context = {
        'products': Product.objects.all()
    }




class ProductDetail(generic.DetailView):
    template_name = 'product_temp/product_detail_view.html'
    model = Product
    context_object_name = 'product'

    def post(self, request, *args, **kwargs):
        resp = JsonResponse({'x': 'y'})
        cart = request.COOKIES.get('cart', '')
        resp.set_cookie('cart', cart + request.POST['products'] + '-')
        return resp


class ProductCardView(generic.DetailView):
    template_name = 'product_temp/product_card_view.html'
    model = Product
    context_object_name = 'product'


class ProductIndexView(generic.TemplateView):
    template_name = 'product_temp/product_index.html'
    extra_context = {
        'products': Product.objects.all()
    }


class ProductScientificView(generic.TemplateView):
    template_name = 'product_temp/product_index_scientific.html'
    extra_context = {
        'products': Product.objects.filter(category__name='scientific')
    }


class ProductHistoricalView(generic.TemplateView):
    template_name = 'product_temp/product_index_historical.html'
    extra_context = {
        'products': Product.objects.filter(category__name='historical')
    }


class ProductArtisticView(generic.TemplateView):
    template_name = 'product_temp/product_index_artistic.html'
    extra_context = {
        'products': Product.objects.filter(category__name='artistic')
    }

def scookie(request):
    response = HttpResponse('cookie')
    response.set_cookie('x', 'y')
    return response


def gcookie(request):
    my_y = request.COOKIES['x']
    return HttpResponse('this is my y: ' + my_y)


def addcookie(request):
    resp = HttpResponse('successfully added to cart')
    cart = request.COOKIES.get('cart', '')
    resp.set_cookie('cart', cart + 'zzz')
    # resp.set_cookie('cart', cart + request.POST['zzz'] + ',')
    return resp


def test_cookie(request):
    if not request.COOKIES.get('cart'):
        response = HttpResponse("Visiting for the first time.")
        response.set_cookie('cart', '2,3,4,')
        return response
    else:
        return HttpResponse(f"Your favorite cart is {request.COOKIES['cart']}")




class SearchView(generic.ListView):
    model = Product
    template_name = 'product_temp/search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            res = Product.objects.filter(name__contains=query)
            result = res
        else:
            result = None
        return result










