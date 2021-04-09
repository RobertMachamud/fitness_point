from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_nr', 'date',
                       'delivery', 'order_total',
                       'gr_total', 'original_cart',
                       'stripe_pid')

    fields = ('order_nr', 'date', 'full_name',
              'email', 'phone_nr', 'country',
              'postcode', 'city', 'street_address1',
              'street_address2', 'county', 'delivery',
              'order_total', 'gr_total', 'original_cart',
              'stripe_pid')

    list_display = ('order_nr', 'date', 'full_name',
                    'order_total', 'delivery',
                    'gr_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
