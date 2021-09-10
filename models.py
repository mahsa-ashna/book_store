from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _





class Product(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=50, help_text=_('Name of the product'))
    price = models.PositiveIntegerField(_('Price'), help_text=_('Input positive amount in Toomaan/1000'))

    leftovers = models.PositiveIntegerField(_('Leftovers'), help_text=_('Input positive amount'))
    sold = models.PositiveIntegerField(verbose_name=_('Sold items'), default=0)

    description = models.CharField(_('Description'), max_length=1000, null=True, blank=True, default=None)
    image = models.FileField(_('Image'), upload_to='ProductImages/', null=True, blank=True, default=None,
                             help_text=_('Image of the product'))

    category = models.ForeignKey(verbose_name=_('Category'), to='Category', on_delete=models.DO_NOTHING)
    discount = models.ForeignKey(verbose_name=_('Discount'), to='Discount', on_delete=models.DO_NOTHING, default=None,
                                 null=True, blank=True)

    class Meta:
        ordering = ['category']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.id}. {self.name} , ({self.category})'

    def final_price(self):
        if self.discount:
            if self.discount.type == '%':
                if self.discount.amount > 100:
                    raise ValidationError(_('Your discount can\'t be more than 100%'))
                else:
                    ds = self.price * self.discount.amount // 100
                    return (self.price - ds) * 1000
            elif self.discount.type == '$':
                if self.discount.amount > self.price:
                    raise ValidationError(_('Your discount can\'t be more than the price'))
                else:
                    ds = self.discount.amount
                    return (self.price - ds) * 1000
        else:
            return self.price * 1000


class Category(models.Model):
    name = models.CharField(verbose_name=_('Name'), help_text=_('Name of the category'), max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'



class Discount(models.Model):
    DISCOUNT_CHOICES = [
        ('%', _('% (Percent)')),
        ('$', _('$ (Toomaan)')),
    ]

    type = models.CharField(verbose_name=_('Type'), max_length=1, choices=DISCOUNT_CHOICES,
                            help_text=_('Type of the discount (percent% or amount$)'))
    name = models.CharField(verbose_name=_('Name'), help_text=_('Name of the discount'), max_length=50, blank=True,
                            null=True, default=None)
    amount = models.PositiveIntegerField(_('Discount Amount'), help_text=_('Input positive amount'),
                                         validators=[])

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        if self.name:
            return f'{self.name}: {self.amount}{self.type}'
        else:
            return f'{self.amount}{self.type}'
