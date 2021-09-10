from django.contrib import admin

# Register your models here.
from products.models import Product, Category, Discount

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Discount)