from django.contrib import admin
from .models import Offer, Category


class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'is_course',
        'day_one',
        'day_two',
        'day_span',
        'time_one',
        'time_two',
        'image',
    )

    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'user_friendly',
        'name',
    )


admin.site.register(Offer, OfferAdmin)
admin.site.register(Category, CategoryAdmin)
