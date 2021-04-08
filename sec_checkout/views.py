import stripe
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from cart.contexts import cart_content


def sec_checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart")
        return redirect(reverse('offers'))

    curr_cart = cart_content(request)
    gr_total = curr_cart['gr_total']
    stripe_total = round(gr_total * 100)

    order_form = OrderForm()
    template = 'sec_checkout/sec_checkout.html'
    content = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_0SMREd7Vdweb1MGRi8S0EycR00JVzSAs5O',
        'client_secret': 'test secret',
    }

    return render(request, template, content)

# installed stripe, added keys for stripe to settings and upd js"