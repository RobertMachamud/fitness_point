from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from offers.models import Offer


def cart_content(request):

    items_amt = 0
    cart_total = 0
    cart_items = []
    curr_taxes_perc = settings.TAXES_PERC
    cart = request.session.get('cart', {})

    for item_id, data_item in cart.items():
        if isinstance(data_item, int):
            offer = get_object_or_404(Offer, pk=item_id)
            cart_total += data_item * offer.price
            items_amt += data_item
            cart_items.append({
                'item_id': item_id,
                'qty': data_item,
                'offer': offer,
            })
        else:
            offer = get_object_or_404(Offer, pk=item_id)
            for size, qty in data_item['items_by_sz'].items():
                cart_total += qty * offer.price
                items_amt += data_item
                cart_items.append({
                    'item_id': item_id,
                    'offer': offer,
                    'size': size,
                    'qty': qty,
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

    content = {
        'delivery': delivery,
        'gr_total': gr_total,
        'cart_items': cart_items,
        'items_amt': items_amt,
        'for_free_del': for_free_del,
        'free_del': settings.FREE_DEL,
        'price_taxes': price_taxes,
        'curr_taxes_perc': curr_taxes_perc,
    }

    return content
