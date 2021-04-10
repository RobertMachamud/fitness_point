from django.http import HttpResponse
from .models import Order, OrderLineItem
from django.core.mail import send_mail
from django.template.loader import render_to_string
from user_profiles.models import UserProfile
from django.conf import settings
from offers.models import Offer
import json
import time


class StripeWH_Handler:

    """ Handle Stripe webhooks """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):

        """ Sends a confirmation email to the user """

        cust_email = order.email
        subject = render_to_string(
            'sec_checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'sec_checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):

        """ Handle a generic/unknown/unexpected webhook event """

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):

        """ Handle the payment_intent.succeeded webhook from Stripe """

        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        gr_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        user_profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            user_profile = UserProfile.objects.get(user__username=username)
            if save_info:
                user_profile.default_phone_nr = shipping_details.phone
                user_profile.default_country = shipping_details.address.country
                user_profile.default_postcode = shipping_details.address.postal_code
                user_profile.default_city = shipping_details.address.city
                user_profile.default_street_address1 = shipping_details.address.line1
                user_profile.default_street_address2 = shipping_details.address.line2
                user_profile.default_county = shipping_details.address.state
                user_profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_nr__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    gr_total=gr_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Verified order is already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=user_profile,
                    email=billing_details.email,
                    phone_nr=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for item_id, data_item in json.loads(cart).items():
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
                                item_sz=sz,
                            )
                            order_line_item.save()
            except Exception as err:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | \
                        ERROR: {err}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):

        """ Handle the payment_intent.payment_failed webhook from Stripe """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
