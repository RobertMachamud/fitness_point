from django.contrib import admin
from .models import Membership


class MembershipAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'descr',
        'image',
        'discount',
        'duration_days',
        'discount_price',
    )


admin.site.register(Membership, MembershipAdmin)
