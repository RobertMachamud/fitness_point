from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from user_profiles.models import UserProfile
from user_profiles.forms import UserProfileForm
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
    except Exception as err:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=err, status=400)


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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            order = order_form.save()
            for item_id, data_item in cart.items():
                print("DAATAAIITTEEMMM", data_item)
                try:
                    offer = Offer.objects.get(id=item_id)
                    if isinstance(data_item, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            offer=offer,
                            qty=data_item,
                        )
                        order_line_item.save()
                        if offer.name.lower() == "jump rope":
                            print("LLLLLOOOOOOOWWWWWWWEEEEERRRRRR!!!!!")
                    else:
                        for sz, qty in data_item['items_by_sz'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                offer=offer,
                                qty=qty,
                                item_sz=sz,
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

        # Attempt to prefill the form with any info
        # the user maintains in their profile
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'f_name': user_profile.user.default_f_name,
                    'email': user_profile.user.email,
                    'phone_nr': user_profile.default_phone_nr,
                    'country': user_profile.default_country,
                    'postcode': user_profile.default_postcode,
                    'city': user_profile.default_city,
                    'street_address1': user_profile.default_street_address1,
                    'street_address2': user_profile.default_street_address2,
                    'county': user_profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        print("OOORRRDDDERRRRR", order.lineitems, profile.is_member)

        # for i, j in order.lineitems.all:
        #     print("LOOOOOOP", i, j)
        # !!!!!!!!!! maybe here - execute toggle_membership function
        # maybe create var bool. - if order.smth. includes membership etc -> change profile_data.is_member

        # Save the user's info
        if save_info:
            profile_data = {
                'default_f_name': order.f_name,
                'default_phone_nr': order.phone_nr,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_city': order.city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
                # 'is_member': var* / if/else oneline - var,
            }

            # if memebership in cart - set countdown for membership var

            # !!!!! changed not yet
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        This is your Order Number: {order_nr}. A confirmation \
        email will be sent to {order.email}. Thank You Very Much!')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'sec_checkout/checkout_successful.html'
    content = {
        'order': order,
        'taxes': settings.TAXES_PERC,
    }
    print(content)
    return render(request, template, content)
