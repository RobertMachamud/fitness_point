from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from offers.models import Offer
from cart.contexts import cart_content
import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def sec_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_nr': request.POST['phone_nr'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'city': request.POST['city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, data_item in cart.items():
                try:
                    offer = Offer.objects.get(id=item_id)
                    if isinstance(data_item, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            offer=offer,
                            qty=data_item,
                        )
                        order_line_item.save()
                    else:
                        for sz, qty in data_item['items_by_sz'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                offer=offer,
                                qty=qty,
                                offer_sz=sz,
                            )
                            order_line_item.save()
                except Offer.DoesNotExist:
                    messages.error(request, (
                        "One of the offers in your cart \
                         wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('to_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_successful', args=[order.order_nr]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(
                request, "There's nothing in your cart at the moment")
            return redirect(reverse('offers'))

        curr_cart = cart_content(request)
        gr_total = curr_cart['gr_total']
        stripe_total = round(gr_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            You probably forgot to set it in your environment.')

    template = 'sec_checkout/sec_checkout.html'
    content = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, content)


def checkout_successful(request, order_nr):

    """ Handles successful checkouts """

    save_info = request.session.get('save-info')
    order = get_object_or_404(Order, order_nr=order_nr)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_nr}. A confirmation \
        email will be sent to {order.email}. Thank You!')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'sec_checkout/checkout_successful.html'
    content = {
        'order': order,
    }
    return render(request, template, content)
