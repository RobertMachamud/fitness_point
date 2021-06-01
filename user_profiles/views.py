from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from sec_checkout.models import Order
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def user_profile(request):

    """ Displays the user's profile. """

    user_profile = get_object_or_404(UserProfile, user=request.user)
    # user_member = str(user_profile.is_member)

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
        'on_profile_page': True,
        'user_member': user_profile.is_member,
    }
    return render(request, template, content)


def order_history(request, order_nr):
    order = get_object_or_404(Order, order_nr=order_nr)

    messages.info(request, (
        f'This is a past confirmation for Order Number {order_nr}. \
        A confirmation email was sent on the order date.'
    ))

    template = 'sec_checkout/checkout_successful.html'
    content = {
        'order': order,
        'from_profile': True,
    }
    return render(request, template, content)


# changed
# form to toggle_ func. - need to save first | mabe make form to link
# (user_profile) or somehow return/render the func.
@login_required
def toggle_membership(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.is_member is True:
        user_profile.is_member = False
        user_profile.save()
        # need to save it
    elif user_profile.is_member is False:
        user_profile.is_member = True
        user_profile.save()

    # Displays message to inform the user about membership update
    # create variable depending if is_member true/false. string - for below
    # messages.success(request, f'Membership updated {user_profile.is_member}')

    if user_profile.is_member:
        messages.success(request, f'Congratulations, you are a Member now!')
    else:
        messages.success(request, f'We are sorry, your Membership ended.')

    form = UserProfileForm(instance=user_profile)
    orders = user_profile.orders.all()
    template = 'user_profiles/user_profile.html'
    content = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
        'user_member': user_profile.is_member,
    }
    return render(request, template, content)
