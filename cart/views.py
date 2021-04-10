from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from offers.models import Offer


def to_cart(request):

    """ A view that renders the cart page """

    return render(request, 'cart/cart.html')


def add_item_to_cart(request, item_id):

    """ Adds a quantity of the selected item to the cart """

    item_sz = None
    qty = int(request.POST.get('qty'))
    cart = request.session.get('cart', {})
    curr_url = request.POST.get('curr_url')
    offer = get_object_or_404(Offer, pk=item_id)

    if 'item_sz' in request.POST:
        item_sz = request.POST['item_sz']
    cart = request.session.get('cart', {})

    if item_sz:
        if item_id in list(cart.keys()):
            if item_sz in cart[item_id]['items_by_sz'].keys():
                cart[item_id]['items_by_sz'][item_sz] += qty
                messages.success(
                    request, f'Updated size {item_sz.upper()} {offer.name} quantity to {cart[item_id]["items_by_sz"][item_sz]}')
            else:
                cart[item_id]['items_by_sz'][item_sz] = qty
                messages.success(
                    request, f'Added size {item_sz.upper()} {offer.name} to your cart')
        else:
            cart[item_id] = {'items_by_sz': {item_sz: qty}}
            messages.success(
                request, f'Added size {item_sz.upper()} {offer.name} to your cart')
    elif not item_sz:
        if item_id in list(cart.keys()):
            cart[item_id] += qty
            messages.success(
                request, f'Updated {offer.name} quantity to {cart[item_id]}')
        else:
            cart[item_id] = qty
            messages.success(request, f'Added {offer.name} to your cart')

    request.session['cart'] = cart
    return redirect(curr_url)


def adj_cart(request, item_id):

    """ Adjusts the quantity of item to specified amount """

    item_sz = None
    qty = int(request.POST.get('qty'))
    offer = get_object_or_404(Offer, pk=item_id)

    if 'item_sz' in request.POST:
        item_sz = request.POST['item_sz']
    cart = request.session.get('cart', {})

    if item_sz:
        if qty > 0:
            cart[item_id]['items_by_sz'][item_sz] = qty
            messages.success(
                request, f'Updated size {item_sz.upper()} {offer.name.upper().upper()} quantity to {cart[item_id]["items_by_sz"][item_sz]}')
        else:
            del cart[item_id]['items_by_sz'][item_sz]
            if not cart[item_id]['items_by_sz']:
                cart.pop(item_id)
            messages.success(
                request, f'Removed size {item_sz.upper()} {offer.name.upper()} from your cart')
    else:
        if qty > 0:
            cart[item_id] = qty
            messages.success(
                request, f'Updated {offer.name.upper()} quantity to {cart[item_id]}')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {offer.name.upper()} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('to_cart'))


def rem_from_cart(request, item_id):

    """ Removes the item from the cart """

    try:
        item_sz = None
        offer = get_object_or_404(Offer, pk=item_id)

        if 'item_sz' in request.POST:
            item_sz = request.POST['item_sz']
        cart = request.session.get('cart', {})

        if item_sz:
            del cart[item_id]['items_by_sz'][item_sz]
            if not cart[item_id]['items_by_sz']:
                cart.pop(item_id)
            messages.success(
                request, f'Removed size {item_sz.upper()} {offer.name.upper()} from your cart')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {offer.name.upper()} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as err:
        messages.error(request, f'Error removing item: {err}')
        return HttpResponse(status=500)
