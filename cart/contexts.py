from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from offers.models import Offer


def cart_content(request):

    items_amt = 0
    cart_total = 0
    cart_items = []
    curr_taxes_prec = settings.TAXES_PERC
    cart = request.session.get('cart', {})

    for item_id, qty in cart.items():
        offer = get_object_or_404(Offer, pk=item_id)
        cart_total += qty * offer.price
        items_amt += qty
        cart_items.append({
            'item_id': item_id,
            'qty': qty,
            'offer': offer
        })

    if cart_total < settings.FREE_DEL:
        delivery = cart_total + Decimal(settings.DEL_COSTS)
        for_free_del = settings.FREE_DEL - cart_total
    else:
        delivery = 0
        for_free_del = 0

    # gr_total = cart_total + delivery

    total = cart_total + delivery
    price_taxes = ((cart_total + delivery) * settings.TAXES_PERC) / 100
    gr_total = total + price_taxes

    context = {
        'delivery': delivery,
        'gr_total': gr_total,
        'cart_items': cart_items,
        'items_amt': items_amt,
        'for_free_del': for_free_del,
        'free_del': settings.FREE_DEL,
        # 'price_taxes': price_taxes,
        'curr_taxes_prec': curr_taxes_prec,
    }

    return context
