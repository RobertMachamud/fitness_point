from django.shortcuts import render, redirect


def to_cart(request):

    """ A view that renders the cart page """

    return render(request, 'cart/cart.html')


def add_item_to_cart(request, item_id):

    """ Adds a quantity of the selected item to the cart """

    qty = int(request.POST.get('qty'))
    cart = request.session.get('cart', {})
    curr_url = request.POST.get('curr_url')

    if item_id in list(cart.keys()):
        cart[item_id] += qty
    else:
        cart[item_id] = qty

    request.session['cart'] = cart
    print("BBBBBBBBBBBBBBBBBBBBBBBB", request.session['cart'])
    return redirect(curr_url)
