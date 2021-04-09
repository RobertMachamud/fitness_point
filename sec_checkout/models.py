import uuid
from decimal import Decimal
from django.db import models
from offers.models import Offer
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField


class Order(models.Model):
    order_nr = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_nr = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    gr_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_nr(self):

        """ Generates a random, unique order number using UUID """

        return uuid.uuid4().hex.upper()

    def update_total(self):

        """ Updates grand total each time a line item is added,
        accounting for delivery costs. """

        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DEL:
            self.delivery = settings.DEL_COSTS
        else:
            self.delivery = 0
        self.gr_total = self.order_total + Decimal(self.delivery)
        self.save()

    def save(self, *args, **kwargs):

        """ Overrides the original save method to set the order number
        if it hasn't been set already. """

        if not self.order_nr:
            self.order_nr = self._generate_order_nr()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_nr


class OrderLineItem(models.Model):
    qty = models.IntegerField(null=False, blank=False, default=0)
    item_sz = models.CharField(max_length=4, null=True, blank=True)
    offer = models.ForeignKey(
        Offer, null=False, blank=False, on_delete=models.CASCADE)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')

    def save(self, *args, **kwargs):

        """ Overrides the original save method to set the lineitem total
        and update the order total. """

        self.lineitem_total = self.offer.price * self.qty
        super().save(*args, **kwargs)


    # Not sure to include it 
    # def __str__(self):
    #     return f'SKU {self.offer.sku} on order {self.order.order_nr}'
