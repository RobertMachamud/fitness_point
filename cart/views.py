from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from offers.models import Offer


def to_cart(request):

    """ A view that renders the cart page """

    return render(request, 'cart/cart.html')


def add_item_to_cart(request, item_id):

    """ Adds a quantity of the selected item to the cart """

    item_size = None
    qty = int(request.POST.get('qty'))
    cart = request.session.get('cart', {})
    curr_url = request.POST.get('curr_url')

    if 'item_size' in request.POST:
        item_size = request.POST['item_size']
    cart = request.session.get('cart', {})

    if item_size:
        if item_id in list(cart.keys()):
            if item_size in cart[item_id]['items_by_sz'].keys():
                cart[item_id]['items_by_sz'][item_size] += qty
                messages.success(
                    request, f'Updated size {item_size.upper()} {offer.name} quantity to {cart[item_id]["items_by_sz"][item_size]}')
            else:
                cart[item_id]['items_by_sz'][item_size] = qty
                messages.success(
                    request, f'Added size {item_size.upper()} {offer.name} to your cart')
        else:
            cart[item_id] = {'items_by_sz': {item_size: qty}}
            messages.success(
                request, f'Added size {item_size.upper()} {offer.name} to your cart')
    elif not item_size:
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

    item_size = None
    qty = int(request.POST.get('qty'))
    offer = get_object_or_404(Offer, pk=item_id)

    if 'item_size' in request.POST:
        item_size = request.POST['item_size']
    cart = request.session.get('cart', {})

    if item_size:
        if qty > 0:
            cart[item_id]['items_by_sz'][item_size] = qty
            messages.success(
                request, f'Updated size {item_size.upper()} {offer.name} quantity to {cart[item_id]["items_by_sz"][item_size]}')
        else:
            del cart[item_id]['items_by_sz'][item_size]
            if not cart[item_id]['items_by_sz']:
                cart.pop(item_id)
            messages.success(
                request, f'Removed size {item_size.upper()} {offer.name} from your cart')
    else:
        if qty > 0:
            cart[item_id] = qty
            messages.success(
                request, f'Updated {offer.name} quantity to {cart[item_id]}')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {offer.name} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('to_cart'))


def rem_from_cart(request, item_id):

    """ Removes the item from the cart """

    try:
        item_size = None
        offer = get_object_or_404(Offer, pk=item_id)

        if 'item_size' in request.POST:
            item_size = request.POST['item_size']
        cart = request.session.get('cart', {})

        if item_size:
            del cart[item_id]['items_by_sz'][item_size]
            if not cart[item_id]['items_by_sz']:
                cart.pop(item_id)
            messages.success(
                request, f'Removed size {item_size.upper()} {offer.name} from your cart')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {offer.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as err:
        messages.error(request, f'Error removing item: {err}')
        return HttpResponse(status=500)
