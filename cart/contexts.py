from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from user_profiles.models import UserProfile
from offers.models import Offer


def cart_content(request):

    items_amt = 0
    cart_total = 0
    cart_items = []

    # evtl changed
    user_member = False
    user_profile = False
    curr_taxes_perc = settings.TAXES_PERC
    cart = request.session.get('cart', {})

    # percentage of discount
    discount = settings.DISCOUNT_PERCENTAGE
    #
    # if request.user.is_authenticated():
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
    except TypeError:
        user_profile = False

    if user_profile:
        user_member = user_profile.is_member

    for item_id, data_item in cart.items():

        # check cart for membership or !maybe local st. or smth.
        # 


        if isinstance(data_item, int):
            offer = get_object_or_404(Offer, pk=item_id)
            if user_member and not offer.is_course:
                cart_total += data_item * (
                    offer.price - (offer.price / 100 * 10))
            elif user_member and offer.is_course:
                cart_total += 0
            elif not user_member:
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
                offer = get_object_or_404(Offer, pk=item_id)

                if user_member and not offer.is_course:
                    cart_total += qty * (
                        offer.price - (offer.price / 100 * 10))
                else:
                    cart_total += qty * offer.price

                # !!!
                # maybe declare var like membersh_in_cart = False
                # if detected in cart - var to True - export to template
                # in template - render (if user_member or memb_in_cart)

                # cart_total += qty * offer.price
                items_amt += qty
                cart_items.append({
                    'item_id': item_id,
                    'offer': offer,
                    'size': size,
                    'qty': qty,
                })

    if cart_total < settings.FREE_DEL:
        delivery = Decimal(settings.DEL_COSTS)
        for_free_del = settings.FREE_DEL - cart_total
    else:
        delivery = 0
        for_free_del = 0

    if cart_total == 0 or user_member:
        delivery = 0
        for_free_del = 0

    # if user_member:
    #     delivery = 0

    total = cart_total + delivery
    price_taxes = (cart_total * settings.TAXES_PERC) / 100
    gr_total = total + price_taxes

    content = {
        'gr_total': gr_total,
        'delivery': delivery,
        'discount': discount,
        'items_amt': items_amt,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'user_member': user_member,
        'price_taxes': price_taxes,
        'for_free_del': for_free_del,
        'free_del': settings.FREE_DEL,
        'curr_taxes_perc': curr_taxes_perc,
    }
    return content
