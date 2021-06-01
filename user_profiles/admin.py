from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'default_f_name',
        'default_phone_nr',
        'default_street_address1',
        'default_street_address2',
        'default_city',
        'default_county',
        'default_postcode',
        'default_country',
        'is_member',
    )


admin.site.register(UserProfile, UserProfileAdmin)
