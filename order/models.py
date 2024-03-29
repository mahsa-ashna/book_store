from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from customer.models import User, Address
from products.models import Product


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('O', _('Online')),
        ('C', _('Card (In-person payment)')),
    ]
    STATUS_CHOICES = [
        ('Cn', _('Canceled')),
        ('Ps', _('Posting')),
        ('Pr', _('Processing')),
    ]

    user = models.ForeignKey(to=User, verbose_name=_('User'), on_delete=models.CASCADE)
    payment_type = models.CharField(verbose_name=_('Payment Type'), max_length=1, choices=PAYMENT_CHOICES, default='O')
    status = models.CharField(verbose_name=_('Status'), max_length=2, choices=STATUS_CHOICES,
                              help_text=_('Types of the status'), default='Pr')
    address = models.ForeignKey(to=Address, verbose_name=_('Address'), on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.address = self.user.address_set.all().last()
        super().save(*args, **kwargs)


    class Meta:

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.user}, {self.status} ({self.payment_type})'

    def total_price(self):
        return sum(map(lambda o: o.item_price(), self.orders.all()))

    def total_items(self):
        return sum(map(lambda o: o.number, self.orders.all()))


class OrderItem(models.Model):
    number = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(verbose_name=_('Order'), to=Order, on_delete=models.DO_NOTHING, related_name='orders')
    product = models.ForeignKey(verbose_name=_('Product'), to=Product, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'{self.order}=> {self.product}, {self.number}'

    def item_price(self):
        return self.product.final_price() * self.number

