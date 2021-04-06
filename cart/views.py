from django.shortcuts import render


def to_cart(request):

    """ A view that renders the cart page """

    return render(request, 'cart/cart.html')
