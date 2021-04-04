from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=254)
    user_friendly = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_user_friendly_name(self):
        return self.user_friendly


class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    descr = models.TextField()
    is_course = models.BooleanField(default=True, null=True, blank=True)
    for_beginners = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)    
    day_one = models.CharField(max_length=254, null=True, blank=True)
    day_two = models.CharField(max_length=254, null=True, blank=True)
    day_span = models.CharField(max_length=254, null=True, blank=True)
    time_one = models.CharField(max_length=254, null=True, blank=True)
    time_two = models.CharField(max_length=254, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name