
from django.shortcuts import render, get_object_or_404
from sec_checkout.models import Order
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


def user_profile(request):

    """ Displays the user's profile. """

    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=user_profile)

    orders = user_profile.orders.all()

    template = 'user_profiles/user_profile.html'
    content = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }
    return render(request, template, content)


def order_history(request, order_nr):
    order = get_object_or_404(Order, order_nr=order_nr)

    messages.info(request, (
        f'This is a past confirmation for order number {order_nr}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'sec_checkout/checkout_successful.html'
    content = {
        'order': order,
        'from_profile': True,
    }
    return render(request, template, content)
