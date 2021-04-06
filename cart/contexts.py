from decimal import Decimal
from django .conf import settings


def cart_content(request):

    cart_total = 0
    products_atm = 0
    cart_items = []

    if cart_total < settings.FREE_DEL:
        delivery = cart_total + Decimal(settings.DEL_COSTS)
        for_free_del = settings.FREE_DEL - cart_total
    else:
        delivery = 0
        for_free_del = 0

    gr_total = cart_total + delivery

    # total = cart_total + delivery
    # price_taxes = ((cart_total + delivery) * settings.TAXES_PERC) / 100
    # gr_total = total + price_taxes

    context = {
        'delivery': delivery,
        'gr_total': gr_total,
        'cart_items': cart_items,
        'products_atm': products_atm,
        'for_free_del': for_free_del,
        'free_del': settings.FREE_DEL,
        # 'price_taxes': price_taxes,
    }

    return context
