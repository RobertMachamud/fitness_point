from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def sec_checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart")
        return redirect(reverse('offers'))

    order_form = OrderForm()
    template = 'sec_checkout/sec_checkout.html'
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)
