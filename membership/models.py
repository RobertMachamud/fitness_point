from django.db import models


# changed
class Membership(models.Model):
    descr = models.TextField()
    name = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.BooleanField(default=False, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_days = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name
